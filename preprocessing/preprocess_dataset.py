
from pathlib import Path
from collections import defaultdict
import csv
import traceback

try:
    from satellite_preprocess import preprocess_pair
except ImportError:
    from preprocessing.satellite_preprocess import preprocess_pair


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

MANIFEST_FILE = PROCESSED_DIR / "dataset_manifest.csv"


# ============================================================
# MULTI-HAZARD CATEGORIES
# ============================================================

HAZARDS = [
    "vegetation",
    "drought",
    "flood"
]

SUPPORTED_EXTENSIONS = {
    ".tif",
    ".tiff"
}


# ============================================================
# FIND SATELLITE IMAGES
# ============================================================

def find_images(folder):
    """
    Find all supported GeoTIFF images recursively.
    """

    images = []

    if not folder.exists():
        return images

    for file in folder.rglob("*"):

        if (
            file.is_file()
            and file.suffix.lower() in SUPPORTED_EXTENSIONS
        ):
            images.append(file)

    return sorted(images)


# ============================================================
# INDEX FILES FOR PAIRING
# ============================================================

def create_file_index(files, base_folder):
    """
    Index images using their relative paths and filenames.

    This allows historical and recent images to be paired
    even when their extensions differ (.tif / .tiff).
    """

    index = defaultdict(list)

    for file in files:

        relative_path = file.relative_to(base_folder)

        key = relative_path.with_suffix("").as_posix().lower()

        index[key].append(file)

    return index


# ============================================================
# PROCESS ONE HAZARD CATEGORY
# ============================================================

def process_hazard(hazard):

    total = 0
    skipped = 0
    failed = 0

    records = []

    historical_raw = RAW_DIR / hazard / "historical"
    recent_raw = RAW_DIR / hazard / "recent"

    historical_processed = (
        PROCESSED_DIR / hazard / "historical"
    )

    recent_processed = (
        PROCESSED_DIR / hazard / "recent"
    )

    # --------------------------------------------------------
    # Create output folders
    # --------------------------------------------------------

    historical_processed.mkdir(
        parents=True,
        exist_ok=True
    )

    recent_processed.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n" + "=" * 70)
    print(f"PROCESSING HAZARD: {hazard.upper()}")
    print("=" * 70)

    # --------------------------------------------------------
    # Validate input directories
    # --------------------------------------------------------

    if not historical_raw.exists():

        print(f"Missing historical folder: {historical_raw}")

        return total, skipped, failed, records

    if not recent_raw.exists():

        print(f"Missing recent folder: {recent_raw}")

        return total, skipped, failed, records

    # --------------------------------------------------------
    # Find images
    # --------------------------------------------------------

    historical_files = find_images(historical_raw)
    recent_files = find_images(recent_raw)

    print(f"Historical images: {len(historical_files)}")
    print(f"Recent images: {len(recent_files)}")

    # --------------------------------------------------------
    # Create image indexes
    # --------------------------------------------------------

    historical_index = create_file_index(
        historical_files,
        historical_raw
    )

    recent_index = create_file_index(
        recent_files,
        recent_raw
    )

    # --------------------------------------------------------
    # Match historical and recent images
    # --------------------------------------------------------

    for key, historical_matches in historical_index.items():

        recent_matches = recent_index.get(key, [])

        if len(historical_matches) != 1 or len(recent_matches) != 1:

            print(f"\nWARNING: Invalid or ambiguous pair: {key}")

            skipped += 1
            continue

        historical_file = historical_matches[0]
        recent_file = recent_matches[0]

        relative_path = historical_file.relative_to(
            historical_raw
        )

        # ----------------------------------------------------
        # Output paths
        # ----------------------------------------------------

        historical_output = (
            historical_processed /
            relative_path.parent /
            f"{historical_file.stem}_processed.tif"
        )

        recent_output = (
            recent_processed /
            relative_path.parent /
            f"{recent_file.stem}_processed.tif"
        )

        historical_output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        recent_output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        print("\n" + "-" * 60)

        print(f"Hazard:      {hazard}")
        print(f"Historical:  {historical_file.name}")
        print(f"Recent:       {recent_file.name}")

        # ----------------------------------------------------
        # Preprocess image pair
        # ----------------------------------------------------

        try:

            preprocess_pair(
                historical_file,
                recent_file,
                historical_output,
                recent_output
            )

            if not historical_output.exists():
                raise RuntimeError(
                    "Historical output was not created."
                )

            if not recent_output.exists():
                raise RuntimeError(
                    "Recent output was not created."
                )

            total += 1

            print("STATUS: SUCCESS")

            records.append({
                "hazard": hazard,
                "pair_id": f"{hazard}_{key}",
                "historical_image": str(
                    historical_output.relative_to(PROJECT_ROOT)
                ),
                "recent_image": str(
                    recent_output.relative_to(PROJECT_ROOT)
                ),
                "status": "success"
            })

        except Exception as error:

            failed += 1

            print("STATUS: FAILED")
            print(f"Reason: {error}")

            traceback.print_exc()

            records.append({
                "hazard": hazard,
                "pair_id": f"{hazard}_{key}",
                "historical_image": str(historical_file),
                "recent_image": str(recent_file),
                "status": "failed"
            })

    # --------------------------------------------------------
    # Check unmatched recent images
    # --------------------------------------------------------

    for key in recent_index:

        if key not in historical_index:

            print(
                f"\nWARNING: No historical match for recent image: {key}"
            )

            skipped += 1

    return total, skipped, failed, records


# ============================================================
# SAVE DATASET MANIFEST
# ============================================================

def save_manifest(records):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "hazard",
        "pair_id",
        "historical_image",
        "recent_image",
        "status"
    ]

    with open(
        MANIFEST_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"\nDataset manifest saved: {MANIFEST_FILE}")


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    grand_total = 0
    grand_skipped = 0
    grand_failed = 0

    all_records = []

    print("\n" + "=" * 70)
    print("MULTI-HAZARD SATELLITE DATASET PREPROCESSING")
    print("=" * 70)

    print(f"\nProject root: {PROJECT_ROOT}")
    print(f"Raw directory: {RAW_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")

    # --------------------------------------------------------
    # Process all hazards
    # --------------------------------------------------------

    for hazard in HAZARDS:

        total, skipped, failed, records = process_hazard(
            hazard
        )

        grand_total += total
        grand_skipped += skipped
        grand_failed += failed

        all_records.extend(records)

    # --------------------------------------------------------
    # Save manifest
    # --------------------------------------------------------

    save_manifest(all_records)

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MULTI-HAZARD PREPROCESSING COMPLETE")
    print("=" * 70)

    print(f"Successfully processed pairs: {grand_total}")
    print(f"Skipped pairs:                {grand_skipped}")
    print(f"Failed pairs:                 {grand_failed}")

    print("\nHAZARD-WISE SUMMARY")

    for hazard in HAZARDS:

        count = sum(
            1 for record in all_records
            if record["hazard"] == hazard
            and record["status"] == "success"
        )

        print(f"{hazard.upper():15} : {count} pairs")

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
