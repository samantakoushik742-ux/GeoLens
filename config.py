import os


def _read_host():
    return os.getenv("HOST") or os.getenv("FLASK_RUN_HOST") or "127.0.0.1"


def _read_port():
    value = os.getenv("PORT") or os.getenv("FLASK_RUN_PORT") or "5000"
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid PORT value: {value!r}. Expected an integer between 1 and 65535.") from exc
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid PORT value: {value!r}. Expected an integer between 1 and 65535.")
    return port


HOST = _read_host()
PORT = _read_port()

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
