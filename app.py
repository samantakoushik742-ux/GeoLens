import json
import logging
import socket
import sys
import traceback
import uuid
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image
from werkzeug.utils import secure_filename

from config import (
    ALLOWED_EXTENSIONS,
    HAZARDS,
    HOST,
    MAX_CONTENT_LENGTH,
    MAX_UPLOAD_BYTES,
    PORT,
)
from predict import DEFAULT_MODEL, EXPECTED_CLASSES, run_pair_inference


PROJECT_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"
HISTORY_FILE = PROJECT_ROOT / "data" / "analysis_history.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("geolens")

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}}
)


def json_error(error, message, status):
    logger.error("%s — %s", error, message)
    return jsonify({
        "success": False,
        "error": error,
        "message": message
    }), status


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def allowed_file(filename):
    suffix = Path(filename).suffix.lower()
    return suffix in ALLOWED_EXTENSIONS


def model_status():
    exists = DEFAULT_MODEL.exists()
    return {
        "available": exists,
        "path": str(DEFAULT_MODEL),
        "architecture": "TemporalDisasterCNN",
        "classes": list(EXPECTED_CLASSES),
        "separate_models": {
            "flood": False,
            "drought": False,
            "vegetation": False
        },
        "note": (
            "A single multi-hazard CNN classifies a temporal pair "
            "as vegetation, drought, or flood. Separate hazard "
            "models are not present."
        )
    }


def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)
        if isinstance(records, list):
            return records
    except (OSError, json.JSONDecodeError) as error:
        logger.error("Could not read analysis history: %s", error)

    return []


def save_history_record(record):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    records = load_history()
    records.insert(0, record)
    records = records[:50]
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def save_upload(file_storage, prefix):
    if file_storage is None or not file_storage.filename:
        raise ValueError("Both historical and recent images are required.")

    original_name = secure_filename(file_storage.filename)
    if not original_name or not allowed_file(original_name):
        raise ValueError(
            "Unsupported file type. Use GeoTIFF, PNG, JPEG, BMP, or WebP."
        )

    file_storage.stream.seek(0, 2)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)

    if size <= 0:
        raise ValueError(f"{original_name} is empty.")

    if size > MAX_UPLOAD_BYTES:
        raise ValueError(
            f"{original_name} exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit."
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(original_name).suffix.lower()
    stored_name = f"{prefix}_{uuid.uuid4().hex}{suffix}"
    destination = UPLOAD_DIR / stored_name
    file_storage.save(destination)
    return destination, original_name, size


def create_preview(path):
    path = Path(path)
    suffix = path.suffix.lower()

    try:
        if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".webp"}:
            with Image.open(path) as img:
                img = img.convert("RGB")
                img.thumbnail((512, 512))
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                return buffer.getvalue()

        import rasterio

        with rasterio.open(path) as src:
            count = src.count
            if count < 1:
                return None
            indexes = list(range(1, min(count, 3) + 1))
            data = src.read(indexes).astype(np.float32)

        if data.ndim == 2:
            data = data[np.newaxis, ...]

        vis = np.zeros((3, data.shape[1], data.shape[2]), dtype=np.float32)
        for index in range(data.shape[0]):
            band = data[index]
            finite = band[np.isfinite(band)]
            if finite.size == 0:
                continue
            low = np.percentile(finite, 2)
            high = np.percentile(finite, 98)
            if high <= low:
                scaled = np.zeros_like(band)
            else:
                scaled = np.clip((band - low) / (high - low), 0, 1)
            vis[index] = scaled
        if data.shape[0] == 1:
            vis[1] = vis[0]
            vis[2] = vis[0]

        image = np.transpose((vis * 255).astype(np.uint8), (1, 2, 0))
        img = Image.fromarray(image, mode="RGB")
        img.thumbnail((512, 512))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as error:
        logger.warning("Preview generation failed for %s: %s", path.name, error)
        return None


def encode_preview(path):
    payload = create_preview(path)
    if payload is None:
        return None
    import base64
    return "data:image/png;base64," + base64.b64encode(payload).decode("ascii")


def selected_hazard_message(hazard, predicted_class, confidence, change_index):
    selected_score_note = (
        "Model confidence is the softmax score for the predicted class, "
        "not a physical disaster probability. "
        f"The temporal change index is {change_index:.2f} and is an "
        "image-difference indicator, not hazard severity."
    )

    if predicted_class == hazard:
        return (
            f"The trained multi-hazard model assigned the pair to "
            f"{predicted_class} with {confidence * 100:.1f}% class confidence. "
            + selected_score_note
        )

    return (
        f"You selected {hazard} monitoring, but the model assigned the "
        f"dominant class {predicted_class} "
        f"({confidence * 100:.1f}% class confidence). "
        + selected_score_note
    )


@app.get("/api/health")
def health():
    status = model_status()
    message = (
        "Backend is running and the trained checkpoint is available."
        if status["available"]
        else (
            "Backend is running. The trained model file is missing. "
            "Train it with: python train.py"
        )
    )
    return jsonify({
        "success": True,
        "status": "ok",
        "host": HOST,
        "port": PORT,
        "model": status,
        "message": message
    })


@app.get("/api/capabilities")
def capabilities():
    status = model_status()
    return jsonify({
        "success": True,
        "hazards": list(HAZARDS),
        "model": status,
        "uploads": {
            "historical_field": "historical",
            "recent_field": "recent",
            "hazard_field": "hazard",
            "max_bytes": MAX_UPLOAD_BYTES,
            "extensions": sorted(ALLOWED_EXTENSIONS)
        },
        "message": status["note"]
    })


@app.get("/api/history")
def history():
    return jsonify({
        "success": True,
        "records": load_history()
    })


@app.post("/api/analyze")
def analyze():
    hazard = (request.form.get("hazard") or "").strip().lower()
    location = (request.form.get("location") or "").strip()

    if hazard not in HAZARDS:
        return json_error(
            "Invalid hazard category",
            "Select flood, drought, or vegetation.",
            400
        )

    try:
        historical_path, historical_name, historical_size = save_upload(
            request.files.get("historical") or request.files.get("image_one"),
            "historical"
        )
        recent_path, recent_name, recent_size = save_upload(
            request.files.get("recent") or request.files.get("image_two"),
            "recent"
        )
    except ValueError as error:
        return json_error("Image validation failed", str(error), 400)

    status = model_status()
    if not status["available"]:
        return json_error(
            "Trained model not found",
            "No checkpoint exists at models/best_multi_hazard_cnn.pth. "
            "Prepare the dataset, then run: python train.py",
            503
        )

    logger.info(
        "Analyze request hazard=%s historical=%s recent=%s",
        hazard,
        historical_name,
        recent_name
    )

    try:
        result = run_pair_inference(
            historical_path,
            recent_path
        )
    except FileNotFoundError as error:
        return json_error("Model loading failed", str(error), 503)
    except ValueError as error:
        logger.error("Preprocessing or validation error:\n%s", traceback.format_exc())
        return json_error(
            "Image preprocessing failed",
            str(error),
            400
        )
    except Exception as error:
        logger.error("Prediction failed:\n%s", traceback.format_exc())
        return json_error(
            "Model inference failed",
            str(error),
            500
        )

    predicted_class = result["predicted_class"]
    confidence = result["confidence"]
    class_probabilities = result["class_probabilities"]
    selected_probability = class_probabilities.get(hazard)

    payload = {
        "success": True,
        "hazard": hazard,
        "prediction": predicted_class,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "selected_hazard_probability": selected_probability,
        "class_probabilities": class_probabilities,
        "change_index": result["change_index"],
        "interpretation": result["interpretation"],
        "message": selected_hazard_message(
            hazard,
            predicted_class,
            confidence,
            result["change_index"]
        ),
        "comparison": {
            "historical": {
                "filename": historical_name,
                "size_bytes": historical_size,
                "preview": encode_preview(historical_path)
            },
            "recent": {
                "filename": recent_name,
                "size_bytes": recent_size,
                "preview": encode_preview(recent_path)
            }
        },
        "model": {
            "architecture": "TemporalDisasterCNN",
            "input_channels": result["input_channels"],
            "image_size": result["image_size"],
            "classes": result["class_names"]
        },
        "location": location or None,
        "timestamp": utc_now()
    }

    save_history_record({
        "id": uuid.uuid4().hex,
        "timestamp": payload["timestamp"],
        "hazard": hazard,
        "location": location or None,
        "prediction": predicted_class,
        "confidence": confidence,
        "selected_hazard_probability": selected_probability,
        "change_index": result["change_index"],
        "historical_image": historical_name,
        "recent_image": recent_name,
        "message": payload["message"]
    })

    return jsonify(payload)


@app.errorhandler(413)
def too_large(_error):
    return json_error(
        "Upload too large",
        f"Each image must be {MAX_UPLOAD_BYTES // (1024 * 1024)} MB or smaller.",
        413
    )


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return json_error(
            "Not found",
            f"No API route matches {request.path}.",
            404
        )
    return error


@app.errorhandler(405)
def method_not_allowed(_error):
    return json_error(
        "Method not allowed",
        f"{request.method} is not allowed for {request.path}.",
        405
    )


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


def port_is_available(host, port):
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        probe.close()


def main():
    if not FRONTEND_DIR.exists():
        print(
            f"ERROR: Frontend directory not found:\n{FRONTEND_DIR}",
            file=sys.stderr
        )
        sys.exit(1)

    if not port_is_available(HOST, PORT):
        print(
            f"ERROR: {HOST}:{PORT} is already in use.\n"
            "Stop the other process occupying this address. "
            "GeoLens will not switch ports automatically.",
            file=sys.stderr
        )
        sys.exit(1)

    print("=" * 70)
    print("GeoLens backend")
    print(f"URL: http://{HOST}:{PORT}")
    print(f"API health: http://{HOST}:{PORT}/api/health")
    print(f"Model: {DEFAULT_MODEL}")
    print(
        "Model status: "
        + ("found" if DEFAULT_MODEL.exists() else "MISSING")
    )
    print("=" * 70)

    app.run(
        host=HOST,
        port=PORT,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":
    main()
