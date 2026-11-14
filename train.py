
from pathlib import Path
import random
import json

import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import DataLoader, Subset

from utils.dataset import TemporalSatelliteDataset
from models.disaster_cnn import TemporalDisasterCNN


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "best_multi_hazard_cnn.pth"

HISTORY_PATH = MODEL_DIR / "training_history.json"


# ============================================================
# MULTI-HAZARD CLASSES
# ============================================================

EXPECTED_CLASSES = [
    "vegetation",
    "drought",
    "flood"
]


# ============================================================
# TRAINING PARAMETERS
# ============================================================

BATCH_SIZE = 8

EPOCHS = 40

LEARNING_RATE = 0.0005

WEIGHT_DECAY = 0.0001

VALIDATION_SPLIT = 0.20

NUM_WORKERS = 0

SEED = 42

PATIENCE = 8


# ============================================================
# REPRODUCIBILITY
# ============================================================

def set_seed(seed=SEED):

    random.seed(seed)

    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():

        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True

    torch.backends.cudnn.benchmark = False


# ============================================================
# DEVICE
# ============================================================

def get_device():

    if torch.cuda.is_available():

        device = torch.device("cuda")

        print("\nGPU detected!")

        print(
            f"GPU: {torch.cuda.get_device_name(0)}"
        )

    else:

        device = torch.device("cpu")

        print("\nCUDA GPU not available.")

        print("Training will use CPU.")

    return device


# ============================================================
# CREATE DATASET
# ============================================================

def create_dataset():

    print("\n" + "=" * 70)

    print("LOADING MULTI-HAZARD DATASET")

    print("=" * 70)

    if not DATA_DIR.exists():

        raise FileNotFoundError(
            f"Processed dataset directory not found: {DATA_DIR}\n\n"
            "Place raw GeoTIFF pairs in:\n"
            "data/raw/<vegetation|drought|flood>/historical/\n"
            "data/raw/<vegetation|drought|flood>/recent/\n\n"
            "Then run:\n"
            "python preprocessing/preprocess_dataset.py"
        )

    dataset = TemporalSatelliteDataset(DATA_DIR)

    if len(dataset) == 0:

        raise RuntimeError(
            "Dataset is empty. Process satellite images first."
        )

    # --------------------------------------------------------
    # Verify classes
    # --------------------------------------------------------

    class_names = list(dataset.class_names)

    print("\nDetected classes:")

    for name in class_names:

        print(f"- {name}")

    if set(class_names) != set(EXPECTED_CLASSES):

        raise RuntimeError(
            "\nDataset classes do not match the multi-hazard "
            "configuration.\n"
            f"Expected: {EXPECTED_CLASSES}\n"
            f"Found: {class_names}"
        )

    print(
        f"\nTotal samples: {len(dataset)}"
    )

    return dataset


# ============================================================
# STRATIFIED TRAIN / VALIDATION SPLIT
# ============================================================

def split_dataset(dataset):

    print("\n" + "=" * 70)

    print("STRATIFIED DATASET SPLITTING")

    print("=" * 70)

    class_indices = {
        i: []
        for i in range(len(dataset.class_names))
    }

    # --------------------------------------------------------
    # Group samples by class
    # --------------------------------------------------------

    for index, sample in enumerate(dataset.samples):

        label = int(sample[2])

        if label not in class_indices:

            raise ValueError(
                f"Invalid label {label} at sample {index}"
            )

        class_indices[label].append(index)

    train_indices = []

    validation_indices = []

    rng = random.Random(SEED)

    # --------------------------------------------------------
    # Split each class separately
    # --------------------------------------------------------

    for class_id, indices in class_indices.items():

        rng.shuffle(indices)

        count = len(indices)

        if count == 0:

            raise RuntimeError(
                f"No samples found for class: "
                f"{dataset.class_names[class_id]}"
            )

        if count < 2:

            raise RuntimeError(
                f"Class {dataset.class_names[class_id]} "
                "needs at least 2 samples for training "
                "and validation."
            )

        validation_count = max(
            1,
            int(round(count * VALIDATION_SPLIT))
        )

        validation_count = min(
            validation_count,
            count - 1
        )

        validation_indices.extend(
            indices[:validation_count]
        )

        train_indices.extend(
            indices[validation_count:]
        )

        print(
            f"{dataset.class_names[class_id]:<15} "
            f"Total: {count:<5} "
            f"Train: {count - validation_count:<5} "
            f"Validation: {validation_count}"
        )

    # --------------------------------------------------------
    # Shuffle final indices
    # --------------------------------------------------------

    rng.shuffle(train_indices)

    rng.shuffle(validation_indices)

    train_dataset = Subset(
        dataset,
        train_indices
    )

    validation_dataset = Subset(
        dataset,
        validation_indices
    )

    print("\nFinal dataset split:")

    print(
        f"Training samples: {len(train_dataset)}"
    )

    print(
        f"Validation samples: {len(validation_dataset)}"
    )

    return train_dataset, validation_dataset


# ============================================================
# CREATE DATALOADERS
# ============================================================

def create_dataloaders(
    train_dataset,
    validation_dataset,
    device
):

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda")
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(device.type == "cuda")
    )

    return train_loader, validation_loader


# ============================================================
# DETECT INPUT CHANNELS
# ============================================================

def detect_channels(dataset):

    historical, recent, label = dataset[0]

    if historical.ndim != 3 or recent.ndim != 3:

        raise RuntimeError(
            "Expected satellite images in CHW format."
        )

    if historical.shape != recent.shape:

        raise RuntimeError(
            "Historical and recent images must have "
            "identical dimensions."
        )

    channels = historical.shape[0]

    print("\nSatellite information:")

    print(f"Input channels: {channels}")

    print(
        f"Image size: "
        f"{historical.shape[1]} x "
        f"{historical.shape[2]}"
    )

    print(f"Sample label: {label}")

    return channels


# ============================================================
# CLASS WEIGHTS
# ============================================================

def calculate_class_weights(
    dataset,
    train_indices
):

    num_classes = len(dataset.class_names)

    class_counts = np.zeros(
        num_classes,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # Count only training samples
    # --------------------------------------------------------

    for index in train_indices:

        label = int(dataset.samples[index][2])

        class_counts[label] += 1

    print("\nTraining class distribution:")

    for index, count in enumerate(class_counts):

        print(
            f"{dataset.class_names[index]:<15}: "
            f"{int(count)}"
        )

    if np.any(class_counts == 0):

        raise RuntimeError(
            "At least one class has no training samples."
        )

    total_samples = class_counts.sum()

    weights = total_samples / (
        num_classes * class_counts
    )

    return torch.tensor(
        weights,
        dtype=torch.float32
    )


# ============================================================
# TRAIN ONE EPOCH
# ============================================================

def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    device
):

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0

    for historical, recent, labels in loader:

        historical = historical.to(
            device,
            non_blocking=True
        )

        recent = recent.to(
            device,
            non_blocking=True
        )

        labels = labels.to(
            device,
            non_blocking=True
        )

        # ----------------------------------------------------
        # Forward pass
        # ----------------------------------------------------

        optimizer.zero_grad(set_to_none=True)

        outputs = model(
            historical,
            recent
        )

        if outputs.ndim != 2:

            raise RuntimeError(
                "Model must return logits with shape [batch, classes]."
            )

        if outputs.shape[1] != len(EXPECTED_CLASSES):

            raise RuntimeError(
                "Model output class count does not match "
                "the three hazard classes."
            )

        loss = criterion(
            outputs,
            labels
        )

        # ----------------------------------------------------
        # Backpropagation
        # ----------------------------------------------------

        loss.backward()

        optimizer.step()

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        batch_size = labels.size(0)

        running_loss += loss.item() * batch_size

        predictions = outputs.argmax(dim=1)

        correct += (
            predictions == labels
        ).sum().item()

        total += batch_size

    epoch_loss = running_loss / total

    epoch_accuracy = (
        correct / total
    ) * 100

    return epoch_loss, epoch_accuracy


# ============================================================
# VALIDATION
# ============================================================

def validate(
    model,
    loader,
    criterion,
    device
):

    model.eval()

    running_loss = 0.0

    correct = 0

    total = 0

    all_predictions = []

    all_labels = []

    with torch.no_grad():

        for historical, recent, labels in loader:

            historical = historical.to(
                device,
                non_blocking=True
            )

            recent = recent.to(
                device,
                non_blocking=True
            )

            labels = labels.to(
                device,
                non_blocking=True
            )

            outputs = model(
                historical,
                recent
            )

            loss = criterion(
                outputs,
                labels
            )

            batch_size = labels.size(0)

            running_loss += (
                loss.item() * batch_size
            )

            predictions = outputs.argmax(dim=1)

            correct += (
                predictions == labels
            ).sum().item()

            total += batch_size

            all_predictions.extend(
                predictions.cpu().tolist()
            )

            all_labels.extend(
                labels.cpu().tolist()
            )

    if total == 0:

        raise RuntimeError(
            "Validation dataset is empty."
        )

    validation_loss = running_loss / total

    validation_accuracy = (
        correct / total
    ) * 100

    return (
        validation_loss,
        validation_accuracy,
        all_predictions,
        all_labels
    )


# ============================================================
# SAVE TRAINING HISTORY
# ============================================================

def save_history(history):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        HISTORY_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


# ============================================================
# SAVE BEST MODEL
# ============================================================

def save_model(
    model,
    optimizer,
    scheduler,
    epoch,
    validation_loss,
    validation_accuracy,
    input_channels,
    class_names
):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    checkpoint = {

        "epoch": epoch,

        "model_state_dict": model.state_dict(),

        "optimizer_state_dict": optimizer.state_dict(),

        "scheduler_state_dict": scheduler.state_dict(),

        "validation_loss": validation_loss,

        "validation_accuracy": validation_accuracy,

        "input_channels": input_channels,

        "num_classes": len(class_names),

        "class_names": class_names,

        "image_size": 256,

        "hazard_type": "multi_hazard",

        "hazards": EXPECTED_CLASSES
    }

    torch.save(
        checkpoint,
        MODEL_PATH
    )

    print(
        f"\nBest model checkpoint saved:\n{MODEL_PATH}"
    )


# ============================================================
# MAIN TRAINING FUNCTION
# ============================================================

def main():

    set_seed()

    # --------------------------------------------------------
    # Device
    # --------------------------------------------------------

    device = get_device()

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    dataset = create_dataset()

    # --------------------------------------------------------
    # Input channels
    # --------------------------------------------------------

    input_channels = detect_channels(dataset)

    num_classes = len(dataset.class_names)

    # --------------------------------------------------------
    # Split dataset
    # --------------------------------------------------------

    train_dataset, validation_dataset = split_dataset(
        dataset
    )

    # --------------------------------------------------------
    # DataLoaders
    # --------------------------------------------------------

    train_loader, validation_loader = create_dataloaders(
        train_dataset,
        validation_dataset,
        device
    )

    # --------------------------------------------------------
    # Class weights
    # --------------------------------------------------------

    class_weights = calculate_class_weights(
        dataset,
        train_dataset.indices
    )

    class_weights = class_weights.to(device)

    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    print("CREATING MULTI-HAZARD TEMPORAL CNN")

    print("=" * 70)

    model = TemporalDisasterCNN(
        in_channels=input_channels,
        num_classes=num_classes
    )

    model = model.to(device)

    print(model)

    # --------------------------------------------------------
    # Loss function
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss(
        weight=class_weights
    )

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY
    )

    # --------------------------------------------------------
    # Learning rate scheduler
    # --------------------------------------------------------

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=3,
        min_lr=0.000001
    )

    # --------------------------------------------------------
    # Training configuration
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    print("TRAINING CONFIGURATION")

    print("=" * 70)

    print(f"Device:          {device}")

    print(f"Classes:         {dataset.class_names}")

    print(f"Batch size:      {BATCH_SIZE}")

    print(f"Epochs:          {EPOCHS}")

    print(f"Learning rate:   {LEARNING_RATE}")

    print(f"Weight decay:    {WEIGHT_DECAY}")

    print(f"Early stopping:  {PATIENCE}")

    print(f"Model path:      {MODEL_PATH}")

    print("=" * 70)

    # --------------------------------------------------------
    # Best model tracking
    # --------------------------------------------------------

    best_validation_loss = float("inf")

    best_validation_accuracy = 0.0

    epochs_without_improvement = 0

    history = {
        "train_loss": [],
        "train_accuracy": [],
        "validation_loss": [],
        "validation_accuracy": []
    }

    # ========================================================
    # TRAINING LOOP
    # ========================================================

    for epoch in range(EPOCHS):

        print(
            f"\nEPOCH {epoch + 1}/{EPOCHS}"
        )

        print("-" * 70)

        # ----------------------------------------------------
        # Training
        # ----------------------------------------------------

        train_loss, train_accuracy = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device
        )

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        (
            validation_loss,
            validation_accuracy,
            predictions,
            actual_labels
        ) = validate(
            model,
            validation_loader,
            criterion,
            device
        )

        # ----------------------------------------------------
        # Learning rate update
        # ----------------------------------------------------

        scheduler.step(validation_loss)

        current_lr = optimizer.param_groups[0]["lr"]

        # ----------------------------------------------------
        # Store history
        # ----------------------------------------------------

        history["train_loss"].append(train_loss)

        history["train_accuracy"].append(train_accuracy)

        history["validation_loss"].append(validation_loss)

        history["validation_accuracy"].append(
            validation_accuracy
        )

        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        print(f"Train Loss:       {train_loss:.4f}")

        print(f"Train Accuracy:   {train_accuracy:.2f}%")

        print(f"Validation Loss:  {validation_loss:.4f}")

        print(
            f"Validation Accuracy: {validation_accuracy:.2f}%"
        )

        print(f"Learning Rate:    {current_lr:.7f}")

        # ----------------------------------------------------
        # Save best model
        # ----------------------------------------------------

        if validation_loss < best_validation_loss:

            best_validation_loss = validation_loss

            best_validation_accuracy = validation_accuracy

            epochs_without_improvement = 0

            save_model(
                model,
                optimizer,
                scheduler,
                epoch + 1,
                validation_loss,
                validation_accuracy,
                input_channels,
                dataset.class_names
            )

        else:

            epochs_without_improvement += 1

            print(
                f"No improvement: "
                f"{epochs_without_improvement}/{PATIENCE}"
            )

        save_history(history)

        # ----------------------------------------------------
        # Early stopping
        # ----------------------------------------------------

        if epochs_without_improvement >= PATIENCE:

            print("\nEarly stopping triggered.")

            break

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n" + "=" * 70)

    print("MULTI-HAZARD MODEL TRAINING COMPLETE")

    print("=" * 70)

    print(
        f"Best validation loss: {best_validation_loss:.4f}"
    )

    print(
        f"Best validation accuracy: "
        f"{best_validation_accuracy:.2f}%"
    )

    print(f"\nModel: {MODEL_PATH}")

    print(f"History: {HISTORY_PATH}")

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()