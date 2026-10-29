
from pathlib import Path
from shutil import copy2
import math

# ============================================================
# 1. DATASET PATHS
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parent

ELECTRONICS_ROOT = Path(
    r"C:\Users\visha\Downloads\Electronic Component Detection.v1i.yolov8"
)

LAB_ROOT = PROJECT_ROOT / "Datasets" / "aria_combined_obb_dataset"

OUTPUT_ROOT = PROJECT_ROOT / "Datasets" / "aria_combined_all_obb_dataset"


SPLITS = ["train", "valid", "test"]

IMAGE_EXTENSIONS = [
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
]

# Electronics classes: original ID -> combined ID
ELECTRONICS_CLASSES = [
    "Arduino",
    "Battery",
    "Display",
    "Esp32",
    "Motor",
    "sensor",
]

# Lab classes: original ID -> combined ID
LAB_CLASSES = [
    "nail",
    "screw",
    "screwdriver",
    "cap",
    "goggles",
    "no_goggles",
    "pen",
]

ALL_CLASSES = ELECTRONICS_CLASSES + LAB_CLASSES


# ============================================================
# 2. HELPERS
# ============================================================

def find_images(folder):
    """Index images by filename stem."""
    result = {}

    if not folder.exists():
        return result

    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            if path.stem in result:
                raise ValueError(
                    f"Duplicate image stem in {folder}: {path.stem}"
                )
            result[path.stem] = path

    return result


def read_label_lines(label_path):
    """Read label lines, or return an empty list if missing."""
    if not label_path.exists():
        return []

    return [
        line.strip()
        for line in label_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def valid_normalized(value):
    return math.isfinite(value) and 0.0 <= value <= 1.0


def convert_electronics_label(line, label_path):
    """
    Convert regular YOLO:
        class x_center y_center width height

    Into OBB:
        class x1 y1 x2 y2 x3 y3 x4 y4

    The converted box is an axis-aligned rectangle.
    """
    parts = line.split()

    if len(parts) != 5:
        raise ValueError(f"Expected 5 values: {label_path}: {line}")

    class_id = int(parts[0])

    if not 0 <= class_id < len(ELECTRONICS_CLASSES):
        raise ValueError(f"Invalid electronics class ID: {label_path}")

    x_center, y_center, width, height = map(float, parts[1:])

    values = [x_center, y_center, width, height]

    if not all(valid_normalized(v) for v in values):
        raise ValueError(f"Invalid normalized YOLO box: {label_path}")

    if width <= 0 or height <= 0:
        raise ValueError(f"Non-positive box size: {label_path}")

    x1 = x_center - width / 2
    y1 = y_center - height / 2
    x2 = x_center + width / 2
    y2 = y_center + height / 2

    # Reject boxes extending outside the image.
    corners = [x1, y1, x2, y1, x2, y2, x1, y2]

    if not all(valid_normalized(v) for v in corners):
        raise ValueError(f"Box extends outside image: {label_path}")

    combined_class = class_id
    output = [combined_class] + corners

    return " ".join(f"{value:.8f}" if i > 0 else str(int(value))
                    for i, value in enumerate(output))


def convert_lab_label(line, label_path):
    """
    Keep lab OBB coordinates, but remap class IDs 0-6 to 6-12.
    Reject malformed or out-of-bounds labels.
    """
    parts = line.split()

    if len(parts) != 9:
        raise ValueError(f"Expected 9 values: {label_path}: {line}")

    class_id = int(parts[0])

    if not 0 <= class_id < len(LAB_CLASSES):
        raise ValueError(f"Invalid lab class ID: {label_path}")

    coords = list(map(float, parts[1:]))

    if not all(valid_normalized(v) for v in coords):
        raise ValueError(f"Out-of-bounds or non-finite OBB: {label_path}")

    combined_class = len(ELECTRONICS_CLASSES) + class_id
    output = [combined_class] + coords

    return " ".join(f"{value:.8f}" if i > 0 else str(int(value))
                    for i, value in enumerate(output))


def write_labels(path, lines):
    path.write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )


# ============================================================
# 3. MERGE A SINGLE DATASET SPLIT
# ============================================================

def merge_split(source_root, source_prefix, split, dataset_type, report):
    images_dir = source_root / split / "images"
    labels_dir = source_root / split / "labels"

    if not images_dir.exists():
        raise FileNotFoundError(f"Missing image folder: {images_dir}")

    if not labels_dir.exists():
        raise FileNotFoundError(f"Missing label folder: {labels_dir}")

    images = find_images(images_dir)
    label_stems = {p.stem for p in labels_dir.glob("*.txt")}

    out_images = OUTPUT_ROOT / split / "images"
    out_labels = OUTPUT_ROOT / split / "labels"

    out_images.mkdir(parents=True, exist_ok=True)
    out_labels.mkdir(parents=True, exist_ok=True)

    copied = 0
    excluded = 0

    for stem, image_path in sorted(images.items()):
        label_path = labels_dir / f"{stem}.txt"
        raw_lines = read_label_lines(label_path)

        converted_lines = []

        try:
            for line in raw_lines:
                if dataset_type == "electronics":
                    converted = convert_electronics_label(line, label_path)
                else:
                    converted = convert_lab_label(line, label_path)

                converted_lines.append(converted)

        except (ValueError, OverflowError) as error:
            excluded += 1
            report.append(
                f"EXCLUDED | {source_prefix} | {split} | "
                f"{image_path.name} | {error}"
            )
            continue

        # Prefix names to avoid filename collisions between datasets.
        new_stem = f"{source_prefix}__{stem}"
        new_image = out_images / f"{new_stem}{image_path.suffix.lower()}"
        new_label = out_labels / f"{new_stem}.txt"

        copy2(image_path, new_image)
        write_labels(new_label, converted_lines)

        copied += 1

    unmatched_labels = sorted(label_stems - set(images.keys()))

    for stem in unmatched_labels:
        report.append(
            f"UNMATCHED LABEL | {source_prefix} | {split} | {stem}.txt"
        )

    print(
        f"{source_prefix:12} {split:5} "
        f"copied={copied:5} excluded={excluded:5} "
        f"unmatched_labels={len(unmatched_labels):4}"
    )

    return copied, excluded


# ============================================================
# 4. MAIN
# ============================================================

def main():
    if not ELECTRONICS_ROOT.exists():
        raise FileNotFoundError(
            f"Electronics dataset not found: {ELECTRONICS_ROOT}"
        )

    if not LAB_ROOT.exists():
        raise FileNotFoundError(f"Lab dataset not found: {LAB_ROOT}")

    # Never overwrite a previous combined dataset.
    if OUTPUT_ROOT.exists():
        raise FileExistsError(
            f"Output folder already exists: {OUTPUT_ROOT}\n"
            "Rename or move it before running this script again."
        )

    # Verify required source folders before starting.
    for root in [ELECTRONICS_ROOT, LAB_ROOT]:
        for split in SPLITS:
            for subfolder in ["images", "labels"]:
                path = root / split / subfolder
                if not path.exists():
                    raise FileNotFoundError(f"Required folder missing: {path}")

    print("Creating combined ARIA OBB dataset...")
    print("Electronics:", ELECTRONICS_ROOT)
    print("Lab dataset:", LAB_ROOT)
    print("Output:", OUTPUT_ROOT)
    print("\nImages with invalid labels will be excluded.")

    report = []
    totals = {"copied": 0, "excluded": 0}

    try:
        for split in SPLITS:
            for root, prefix, dataset_type in [
                (ELECTRONICS_ROOT, "electronics", "electronics"),
                (LAB_ROOT, "lab", "lab"),
            ]:
                copied, excluded = merge_split(
                    root, prefix, split, dataset_type, report
                )
                totals["copied"] += copied
                totals["excluded"] += excluded

        # Use an absolute dataset path to avoid relative-path confusion.
        yaml_path = OUTPUT_ROOT / "data.yaml"
        absolute_path = OUTPUT_ROOT.resolve().as_posix()

        yaml_lines = [
            f"path: {absolute_path}",
            "train: train/images",
            "val: valid/images",
            "test: test/images",
            "",
            "names:",
        ]

        for class_id, class_name in enumerate(ALL_CLASSES):
            yaml_lines.append(f"  {class_id}: {class_name}")

        yaml_path.write_text(
            "\n".join(yaml_lines) + "\n",
            encoding="utf-8",
        )

        report_path = OUTPUT_ROOT / "merge_report.txt"
        report_path.write_text(
            "\n".join(report)
            + ("\n" if report else "No excluded or unmatched files.\n"),
            encoding="utf-8",
        )

    except Exception:
        print(
            "\nMerge stopped because an error occurred. "
            "The source datasets have not been modified."
        )
        raise

    print("\nMerge finished.")
    print("Images copied:", totals["copied"])
    print("Images excluded for invalid labels:", totals["excluded"])
    print("Class count:", len(ALL_CLASSES))
    print("Dataset YAML:", OUTPUT_ROOT / "data.yaml")
    print("Review report:", OUTPUT_ROOT / "merge_report.txt")
    print("\nOriginal datasets and trained checkpoints were not modified.")


if __name__ == "__main__":
    main()
