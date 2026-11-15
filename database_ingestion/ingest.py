from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import shutil
import time
import zipfile
from datetime import date
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

ZIP_PATH = SCRIPT_DIR / os.getenv("INGEST_ZIP_NAME", "dataset.zip")
EXTRACT_DIR = SCRIPT_DIR / "extracted"
RAW_IMPORT_DIR = PROJECT_ROOT / "data" / "raw" / "imported"
CREDENTIALS_FILE = PROJECT_ROOT / os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = PROJECT_ROOT / os.getenv("GOOGLE_TOKEN_FILE", "token.json")
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Sentinel-2 SAFE products commonly contain JP2 bands; GeoTIFFs are also supported.
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif",
    ".tif", ".tiff", ".jp2"
}


def connect_mysql():
    required = ("MYSQL_HOST", "MYSQL_USER", "MYSQL_DATABASE", "MYSQL_SSL_CA")
    missing = [key for key in required if os.getenv(key) in (None, "")]
    if missing:
        raise RuntimeError(f"Missing MySQL environment variables: {', '.join(missing)}")

    port_value = os.getenv("MYSQL_PORT", "3306")
    try:
        port = int(port_value) if port_value not in (None, "") else 3306
    except ValueError as exc:
        raise RuntimeError(f"Invalid MYSQL_PORT value: {port_value!r}") from exc

    if not 1 <= port <= 65535:
        raise RuntimeError(f"Invalid MYSQL_PORT value: {port_value!r}")

    config = {
        "host": os.environ["MYSQL_HOST"],
        "port": port,
        "user": os.environ["MYSQL_USER"],
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ["MYSQL_DATABASE"],
        "connection_timeout": 20,
    }
    config.update(
        ssl_ca=os.environ["MYSQL_SSL_CA"],
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
    return mysql.connector.connect(**config)


def connect_google_drive():
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"Google OAuth credentials file not found: {CREDENTIALS_FILE}\n"
            "Place your Google OAuth desktop-app credentials.json in the project root."
        )

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("drive", "v3", credentials=creds, cache_discovery=False)


def safe_extract_zip(zip_path: Path, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()

    with zipfile.ZipFile(zip_path, "r") as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(root):
                raise ValueError(f"Unsafe ZIP entry blocked: {member.filename}")
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output, length=1024 * 1024)


def find_images():
    return sorted(
        p for p in EXTRACT_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_existing_hashes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT file_hash FROM images WHERE file_hash IS NOT NULL")
    result = {row[0] for row in cursor.fetchall()}
    cursor.close()
    return result


def infer_metadata(path: Path):
    """Infer only simple labels from path/name; leave uncertain metadata NULL."""
    text = str(path).lower()
    hazard = next(
        (name for name in ("flood", "vegetation", "drought") if re.search(rf"\b{name}\b", text)),
        None,
    )

    # Match common Sentinel-2 band naming such as B08, B8A, B04.
    band_match = re.search(r"(?<![a-z0-9])(B(?:0[1-9]|1[0-2]|8A))(?![a-z0-9])", path.stem.upper())
    band = band_match.group(1) if band_match else None

    # Parse YYYYMMDD or YYYY-MM-DD only when present in the filename/path.
    date_match = re.search(r"(?<!\d)(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)(?!\d)", str(path))
    acquired = None
    if date_match:
        try:
            acquired = date(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
        except ValueError:
            acquired = None

    return hazard, acquired, band


def upload_image(service, path: Path):
    mime_type, _ = mimetypes.guess_type(str(path))
    metadata = {"name": path.name}
    media = MediaFileUpload(
        str(path),
        mimetype=mime_type or "application/octet-stream",
        resumable=True,
    )
    result = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,webViewLink",
    ).execute(num_retries=3)
    drive_id = result["id"]
    return drive_id, result.get(
        "webViewLink", f"https://drive.google.com/file/d/{drive_id}/view"
    )


def copy_to_local_raw(path: Path):
    """Keep a local copy under data/raw/imported while preserving ZIP subfolders."""
    relative = path.relative_to(EXTRACT_DIR)
    destination = RAW_IMPORT_DIR / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        shutil.copy2(path, destination)
    return destination


def save_record(conn, path, local_path, drive_id, drive_url, digest):
    hazard, acquired, band = infer_metadata(path)
    relative_source = str(path.relative_to(EXTRACT_DIR))
    query = """
        INSERT INTO images
        (filename, drive_file_id, drive_url, image_path, source_path,
         hazard_type, acquisition_date, band_name, file_hash, file_size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE file_hash = VALUES(file_hash)
    """
    values = (
        path.name, drive_id, drive_url, str(local_path), relative_source,
        hazard, acquired, band, digest, path.stat().st_size,
    )
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    cursor.close()


def main():
    print("\n===== SATELLITE DATA INGESTION =====")
    if not ZIP_PATH.exists():
        raise FileNotFoundError(
            f"Dataset ZIP not found: {ZIP_PATH}\n"
            "Copy your archive to database_ingestion/dataset.zip or set INGEST_ZIP_NAME in .env."
        )

    safe_extract_zip(ZIP_PATH, EXTRACT_DIR)
    images = find_images()
    if not images:
        raise RuntimeError(
            "No supported images found. Supported formats include JP2, TIFF, PNG and JPEG."
        )

    print(f"Images found: {len(images)}")
    conn = connect_mysql()
    try:
        service = connect_google_drive()
        known_hashes = get_existing_hashes(conn)
        uploaded = skipped = failed = 0

        for index, path in enumerate(images, start=1):
            try:
                digest = sha256_file(path)
                if digest in known_hashes:
                    # Still ensure the local copy exists for downstream processing.
                    copy_to_local_raw(path)
                    skipped += 1
                    print(f"[{index}/{len(images)}] Already in database: {path.name}")
                    continue

                local_path = copy_to_local_raw(path)
                drive_id, drive_url = upload_image(service, path)
                save_record(conn, path, local_path, drive_id, drive_url, digest)
                known_hashes.add(digest)
                uploaded += 1
                print(f"[{index}/{len(images)}] Ingested: {path.name}")

            except Exception as exc:
                failed += 1
                print(f"[{index}/{len(images)}] Failed: {path.name} | {exc}")
                time.sleep(1)

        print("\n===== INGESTION SUMMARY =====")
        print(f"Total images: {len(images)}")
        print(f"New uploads: {uploaded}")
        print(f"Already present: {skipped}")
        print(f"Failed: {failed}")
        print(f"Local copies: {RAW_IMPORT_DIR}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
