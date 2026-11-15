import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")


def _read_port():
    value = os.getenv("PORT", "5000")
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Invalid PORT value: {value!r}. "
            "Expected an integer between 1 and 65535."
        ) from exc
    if not 1 <= port <= 65535:
        raise ValueError(
            f"Invalid PORT value: {value!r}. "
            "Expected an integer between 1 and 65535."
        )
    return port


HOST = os.getenv("HOST", "0.0.0.0")
PORT = _read_port()
CORS_ALLOWED_ORIGINS = tuple(
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500,"
        "https://geolens-r130rnnhw-samantakoushik742-uxs-projects.vercel.app"
    ).split(",")
    if origin.strip()
)
CORS_ALLOWED_ORIGIN_REGEX = os.getenv("CORS_ALLOWED_ORIGIN_REGEX") or None

MAX_UPLOAD_BYTES = 50 * 1024 * 1024
MAX_CONTENT_LENGTH = (MAX_UPLOAD_BYTES * 2) + (2 * 1024 * 1024)

ALLOWED_EXTENSIONS = {
    ".tif",
    ".tiff",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp"
}

HAZARDS = ("flood", "drought", "vegetation")
