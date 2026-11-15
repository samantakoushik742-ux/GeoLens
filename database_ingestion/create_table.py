from __future__ import annotations

import os
import mysql.connector
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


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


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS images (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    cloudinary_url TEXT NULL,
    cloudinary_public_id VARCHAR(255) NULL,
    drive_file_id VARCHAR(255) NULL,
    drive_url TEXT NULL,
    image_path TEXT NULL,
    source_path TEXT NULL,
    hazard_type VARCHAR(50) NULL,
    acquisition_date DATE NULL,
    band_name VARCHAR(30) NULL,
    file_hash CHAR(64) NOT NULL UNIQUE,
    file_size BIGINT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_images_hazard_date (hazard_type, acquisition_date),
    INDEX idx_images_drive_file_id (drive_file_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def main():
    conn = connect_mysql()
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        conn.commit()
        cursor.close()
        print("Images table is ready.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
