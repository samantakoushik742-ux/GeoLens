
from pathlib import Path
import argparse
import os

import numpy as np
import torch
import rasterio

from rasterio.enums import Resampling

from models.disaster_cnn import TemporalDisasterCNN

from preprocessing.satellite_preprocess import (
    replace_invalid_values,
    percentile_clip,
    normalize_pair
)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DEFAULT_MODEL = Path(
    os.getenv("GEOLENS_MODEL_PATH")
    or PROJECT_ROOT / "models" / "best_multi_hazard_cnn.pth"
).expanduser()
if not DEFAULT_MODEL.is_absolute():
    DEFAULT_MODEL = PROJECT_ROOT / DEFAULT_MODEL

EXPECTED_CLASSES = [
    "vegetation",
    "drought",
    "flood"
]

DEFAULT_IMAGE_SIZE = 256

GEOTIFF_EXTENSIONS = {".tif", ".tiff"}

OPTICAL_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp"
}


# ============================================================
# DEVICE
# ============================================================

def get_device():

    if torch.cuda.is_available():

        device = torch.device("cuda")

        print(
            f"\nUsing GPU: {torch.cuda.get_device_name(0)}"
        )

    else:

        device = torch.device("cpu")

        print("\nUsing CPU")

    return device


# ============================================================
# LOAD SATELLITE IMAGE
# ============================================================

def load_optical_image(path, size=256):
    """
    Load a browser-uploaded optical image (PNG/JPEG) as CHW float32.
    These files are not georeferenced satellite rasters.
    """

    from PIL import Image

    path = Path(path)

    with Image.open(path) as img:

        original_width, original_height = img.size

        if img.mode == "RGBA":
            img = img.convert("RGB")
        elif img.mode == "L":
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        img = img.resize(
            (size, size),
            Image.Resampling.BILINEAR
        )

        array = np.transpose(
            np.asarray(img, dtype=np.float32),
            (2, 0, 1)
        )

    metadata = {
        "crs": None,
        "bounds": None,
        "width": original_width,
        "height": original_height,
        "bands": int(array.shape[0]),
        "georeferenced": False
    }

    print(f"\nLoaded optical image: {path.name}")
    print(f"Bands: {metadata['bands']}")
    print(
        f"Original size: "
        f"{metadata['width']} x {metadata['height']}"
    )
    print(f"Processed size: {size} x {size}")

    return array, metadata


def load_raster_image(path, size=256):

    path = Path(path)

    with rasterio.open(path) as src:

        if src.count < 1:

            raise ValueError(
                f"No raster bands found in {path}"
            )

        image = src.read(
            out_shape=(
                src.count,
                size,
                size
            ),
            resampling=Resampling.bilinear
        ).astype(np.float32)

        metadata = {
            "crs": src.crs,
            "bounds": src.bounds,
            "width": src.width,
            "height": src.height,
            "bands": src.count,
            "georeferenced": src.crs is not None
        }

    print(f"\nLoaded: {path.name}")
    print(f"Bands: {metadata['bands']}")
    print(
        f"Original size: "
        f"{metadata['width']} x {metadata['height']}"
    )
    print(f"Processed size: {size} x {size}")

    return image, metadata


def load_image(path, size=256):

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(
            f"Satellite image not found:\n{path}"
        )

    suffix = path.suffix.lower()
    errors = []

    if suffix in OPTICAL_EXTENSIONS:

        try:
            return load_optical_image(path, size)
        except Exception as error:
            errors.append(str(error))

    try:
        return load_raster_image(path, size)
    except Exception as error:
        errors.append(str(error))

    if suffix not in OPTICAL_EXTENSIONS:

        try:
            return load_optical_image(path, size)
        except Exception as error:
            errors.append(str(error))

    raise ValueError(
        "Unable to read image "
        f"{path.name}. {errors[-1] if errors else ''}"
    )


# ============================================================
# VALIDATE IMAGE ALIGNMENT
# ============================================================

def validate_alignment(
    historical_metadata,
    recent_metadata
):

    # --------------------------------------------------------
    # Coordinate reference system
    # --------------------------------------------------------

    historical_crs = historical_metadata.get("crs")
    recent_crs = recent_metadata.get("crs")
    historical_georeferenced = bool(
        historical_metadata.get("georeferenced")
    )
    recent_georeferenced = bool(
        recent_metadata.get("georeferenced")
    )

    if not historical_georeferenced and not recent_georeferenced:

        print(
            "\nNo georeferencing metadata found. "
            "Skipping CRS and bounds alignment. "
            "Both images will still be resized and "
            "normalized to the same tensor size."
        )

    elif historical_georeferenced != recent_georeferenced:

        raise ValueError(
            "One image is georeferenced and the other is not. "
            "Use two GeoTIFF files or two optical images."
        )

    elif historical_crs != recent_crs:

        raise ValueError(
            "Historical and recent images use "
            "different coordinate reference systems. "
            "Reproject them before prediction."
        )

    else:

        historical_bounds = historical_metadata["bounds"]
        recent_bounds = recent_metadata["bounds"]
        tolerance = 1e-6

        for old_value, new_value in zip(
            historical_bounds,
            recent_bounds
        ):

            if abs(old_value - new_value) > tolerance:

                raise ValueError(
                    "Historical and recent images cover "
                    "different geographic extents. "
                    "Align them before prediction."
                )

    # --------------------------------------------------------
    # Number of bands
    # --------------------------------------------------------

    if (
        historical_metadata["bands"]
        != recent_metadata["bands"]
    ):

        raise ValueError(
            "Historical and recent images have "
            "different band counts."
        )

    print("\nImage alignment checks passed.")


# ============================================================
# PREPROCESS HISTORICAL AND RECENT IMAGES
# ============================================================

def preprocess_pair(
    historical_path,
    recent_path,
    size=DEFAULT_IMAGE_SIZE
):

    print("\n" + "=" * 70)

    print("PREPROCESSING SATELLITE IMAGE PAIR")

    print("=" * 70)

    # --------------------------------------------------------
    # Load images
    # --------------------------------------------------------

    historical, historical_metadata = load_image(
        historical_path,
        size
    )

    recent, recent_metadata = load_image(
        recent_path,
        size
    )

    # --------------------------------------------------------
    # Validate geographic alignment
    # --------------------------------------------------------

    validate_alignment(
        historical_metadata,
        recent_metadata
    )

    if historical.shape != recent.shape:

        raise ValueError(
            "Historical and recent images "
            "have incompatible shapes."
        )

    # --------------------------------------------------------
    # Replace invalid values
    # --------------------------------------------------------

    historical = replace_invalid_values(
        historical
    )

    recent = replace_invalid_values(
        recent
    )

    # --------------------------------------------------------
    # Percentile clipping
    # --------------------------------------------------------

    historical = percentile_clip(
        historical
    )

    recent = percentile_clip(
        recent
    )

    # --------------------------------------------------------
    # Common normalization
    # --------------------------------------------------------

    historical, recent = normalize_pair(
        historical,
        recent
    )

    # --------------------------------------------------------
    # Check for invalid values
    # --------------------------------------------------------

    if not np.isfinite(historical).all():

        raise ValueError(
            "Historical image contains invalid values "
            "after normalization."
        )

    if not np.isfinite(recent).all():

        raise ValueError(
            "Recent image contains invalid values "
            "after normalization."
        )

    # --------------------------------------------------------
    # Convert to PyTorch tensors
    # --------------------------------------------------------

    historical = torch.from_numpy(
        np.ascontiguousarray(historical)
    ).float()

    recent = torch.from_numpy(
        np.ascontiguousarray(recent)
    ).float()

    # --------------------------------------------------------
    # Add batch dimension
    # --------------------------------------------------------

    historical = historical.unsqueeze(0)

    recent = recent.unsqueeze(0)

    print("\nPreprocessing completed.")

    print(
        f"Tensor shape: {tuple(historical.shape)}"
    )

    return historical, recent


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

def load_model(model_path, device):

    model_path = Path(model_path)

    if not model_path.exists():

        raise FileNotFoundError(
            f"\nTrained model not found:\n{model_path}\n\n"
            "Train the model first using:\n"
            "python train.py"
        )

    print("\nLoading multi-hazard CNN...")

    checkpoint = torch.load(
        model_path,
        map_location=device
    )

    # --------------------------------------------------------
    # Load model configuration
    # --------------------------------------------------------

    input_channels = checkpoint["input_channels"]

    class_names = checkpoint["class_names"]

    num_classes = checkpoint.get(
        "num_classes",
        len(class_names)
    )

    image_size = checkpoint.get(
        "image_size",
        DEFAULT_IMAGE_SIZE
    )

    # --------------------------------------------------------
    # Validate model classes
    # --------------------------------------------------------

    if set(class_names) != set(EXPECTED_CLASSES):

        raise RuntimeError(
            "Checkpoint contains unexpected classes.\n"
            f"Expected: {EXPECTED_CLASSES}\n"
            f"Found: {class_names}"
        )

    if num_classes != len(class_names):

        raise RuntimeError(
            "Checkpoint class count is inconsistent."
        )

    # --------------------------------------------------------
    # Create CNN
    # --------------------------------------------------------

    model = TemporalDisasterCNN(
        in_channels=input_channels,
        num_classes=num_classes
    )

    # --------------------------------------------------------
    # Load weights
    # --------------------------------------------------------

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(device)

    model.eval()

    print("\nModel loaded successfully.")

    print(f"Input channels: {input_channels}")

    print(f"Number of classes: {num_classes}")

    print(f"Classes: {class_names}")

    print(f"Image size: {image_size}")

    print(
        f"Training epoch: {checkpoint.get('epoch', 'Unknown')}"
    )

    print(
        f"Validation accuracy: "
        f"{checkpoint.get('validation_accuracy', 0):.2f}%"
    )

    return (
        model,
        class_names,
        input_channels,
        image_size
    )


# ============================================================
# TEMPORAL CHANGE ANALYSIS
# ============================================================

def calculate_change_score(
    historical,
    recent
):
    """
    Calculate mean absolute difference between
    normalized historical and recent images.

    This is an image-change indicator, not a
    physical percentage of affected land.
    """

    difference = torch.abs(
        recent - historical
    )

    change_score = difference.mean().item()

    change_index = change_score * 100

    return change_index


# ============================================================
# PREDICTION
# ============================================================

def predict(
    model,
    class_names,
    historical,
    recent,
    device
):

    historical = historical.to(device)

    recent = recent.to(device)

    # --------------------------------------------------------
    # Model inference
    # --------------------------------------------------------

    with torch.inference_mode():

        outputs = model(
            historical,
            recent
        )

        if outputs.ndim != 2:

            raise RuntimeError(
                "CNN must return logits with shape "
                "[batch_size, number_of_classes]."
            )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        predicted_index = probabilities.argmax(
            dim=1
        ).item()

    # --------------------------------------------------------
    # Predicted hazard
    # --------------------------------------------------------

    predicted_class = class_names[
        predicted_index
    ]

    confidence = probabilities[
        0,
        predicted_index
    ].item()

    # --------------------------------------------------------
    # Image change
    # --------------------------------------------------------

    change_index = calculate_change_score(
        historical,
        recent
    )

    # --------------------------------------------------------
    # Return results
    # --------------------------------------------------------

    return (
        predicted_class,
        confidence,
        probabilities,
        change_index
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(
    predicted_class,
    confidence,
    probabilities,
    class_names,
    change_index
):

    print("\n")

    print("=" * 70)

    print("MULTI-HAZARD SATELLITE MONITORING RESULTS")

    print("=" * 70)

    # --------------------------------------------------------
    # Predicted condition
    # --------------------------------------------------------

    print(
        f"\nDetected category: {predicted_class.upper()}"
    )

    print(
        f"Model confidence: {confidence * 100:.2f}%"
    )

    print(
        f"Temporal change index: {change_index:.2f}"
    )

    # --------------------------------------------------------
    # Class probabilities
    # --------------------------------------------------------

    print("\nHAZARD CLASS PROBABILITIES")

    print("-" * 45)

    for index, class_name in enumerate(class_names):

        probability = probabilities[
            0,
            index
        ].item()

        print(
            f"{class_name.upper():<18}"
            f"{probability * 100:>8.2f}%"
        )

    print("-" * 45)

    # --------------------------------------------------------
    # Confidence interpretation
    # --------------------------------------------------------

    print("\nMODEL INTERPRETATION")

    if confidence >= 0.80:

        print(
            "The model has high confidence "
            "in its predicted category."
        )

    elif confidence >= 0.60:

        print(
            "The model has moderate confidence. "
            "Further verification is recommended."
        )

    else:

        print(
            "The prediction has low confidence. "
            "Do not rely on this classification alone."
        )

    # --------------------------------------------------------
    # Warning
    # --------------------------------------------------------

    print("\nIMPORTANT NOTES")

    print(
        "1. Model confidence is not disaster probability."
    )

    print(
        "2. Temporal change index is not hazard severity."
    )

    print(
        "3. Verify predictions using appropriate "
        "spectral indices and ground observations."
    )

    print(
        "4. This model predicts one dominant category "
        "among the three trained classes."
    )

    print("=" * 70)


def interpret_confidence(confidence):

    if confidence >= 0.80:
        return (
            "The model has high confidence "
            "in its predicted category."
        )

    if confidence >= 0.60:
        return (
            "The model has moderate confidence. "
            "Further verification is recommended."
        )

    return (
        "The prediction has low confidence. "
        "Do not rely on this classification alone."
    )


def run_pair_inference(
    historical_path,
    recent_path,
    model_path=None,
    size=None
):
    """
    Run the existing temporal CNN on one image pair.
    Returns a serializable result dictionary.
    """

    device = get_device()

    model_file = Path(model_path) if model_path else DEFAULT_MODEL

    (
        model,
        class_names,
        input_channels,
        model_image_size
    ) = load_model(
        model_file,
        device
    )

    image_size = (
        size
        if size is not None
        else model_image_size
    )

    if image_size <= 0:

        raise ValueError(
            "Image size must be greater than zero."
        )

    historical, recent = preprocess_pair(
        historical_path,
        recent_path,
        image_size
    )

    actual_channels = historical.shape[1]

    if actual_channels != input_channels:

        raise ValueError(
            "CHANNEL MISMATCH: "
            f"Model expects {input_channels} bands, "
            f"but the uploaded pair has {actual_channels} bands. "
            "Use the same satellite band configuration "
            "that was used during model training."
        )

    (
        predicted_class,
        confidence,
        probabilities,
        change_index
    ) = predict(
        model,
        class_names,
        historical,
        recent,
        device
    )

    class_probabilities = {
        name: float(probabilities[0, index].item())
        for index, name in enumerate(class_names)
    }

    return {
        "predicted_class": predicted_class,
        "confidence": float(confidence),
        "class_probabilities": class_probabilities,
        "change_index": float(change_index),
        "input_channels": int(input_channels),
        "image_size": int(image_size),
        "class_names": list(class_names),
        "interpretation": interpret_confidence(float(confidence))
    }


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Multi-hazard satellite image prediction "
            "for vegetation, drought and flood monitoring."
        )
    )

    # --------------------------------------------------------
    # Input images
    # --------------------------------------------------------

    parser.add_argument(
        "--historical",
        required=True,
        help="Historical satellite GeoTIFF"
    )

    parser.add_argument(
        "--recent",
        required=True,
        help="Recent satellite GeoTIFF"
    )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    parser.add_argument(
        "--model",
        default=str(DEFAULT_MODEL),
        help="Trained CNN checkpoint"
    )

    # --------------------------------------------------------
    # Image size
    # --------------------------------------------------------

    parser.add_argument(
        "--size",
        type=int,
        default=None,
        help="Optional image size override"
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Device
    # --------------------------------------------------------

    device = get_device()

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    (
        model,
        class_names,
        input_channels,
        model_image_size
    ) = load_model(
        args.model,
        device
    )

    image_size = (
        args.size
        if args.size is not None
        else model_image_size
    )

    if image_size <= 0:

        raise ValueError(
            "Image size must be greater than zero."
        )

    # --------------------------------------------------------
    # Preprocess images
    # --------------------------------------------------------

    historical, recent = preprocess_pair(
        args.historical,
        args.recent,
        image_size
    )

    # --------------------------------------------------------
    # Validate input channels
    # --------------------------------------------------------

    actual_channels = historical.shape[1]

    if actual_channels != input_channels:

        raise ValueError(
            "\nCHANNEL MISMATCH\n\n"
            f"Model expects: {input_channels} bands\n"
            f"Historical image: {actual_channels} bands\n\n"
            "Use the same satellite band configuration "
            "that was used during model training."
        )

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    (
        predicted_class,
        confidence,
        probabilities,
        change_index
    ) = predict(
        model,
        class_names,
        historical,
        recent,
        device
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    display_results(
        predicted_class,
        confidence,
        probabilities,
        class_names,
        change_index
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
