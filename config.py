import os

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 5000))

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
