
from pathlib import Path
from ultralytics import YOLO

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_YAML = (
    PROJECT_ROOT
    / "vision"
    / "Datasets"
    / "aria_combined_obb_dataset"
    / "data.yaml"
)

# Pretrained YOLOv8 OBB model
MODEL_PATH = PROJECT_ROOT / "vision" / "yolov8s-obb.pt"

# Training settings
EPOCHS = 100
IMAGE_SIZE = 640
BATCH_SIZE = 8

if not DATA_YAML.exists():
    raise FileNotFoundError(
        f"Dataset config not found: {DATA_YAML}"
    )

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Pretrained OBB model not found: {MODEL_PATH}"
    )

print("Loading pretrained YOLOv8 OBB model...")
model = YOLO(str(MODEL_PATH))

print("Starting OBB training on the new dataset only...")

model.train(
    data=str(DATA_YAML),
    epochs=EPOCHS,
    imgsz=IMAGE_SIZE,
    batch=BATCH_SIZE,
    workers=0,
    patience=20,
    device=0,
    project=str(
        PROJECT_ROOT
        / "vision"
        / "Datasets"
        / "aria_combined_obb_dataset"
        / "runs"
        / "obb"
    ),
    name="aria_objects",
    exist_ok=True,
    plots=True,
    seed=42,
)

print("Training finished!")

print(
    "Best model:",
    PROJECT_ROOT
    / "vision"
    / "Datasets"
    / "aria_combined_obb_dataset"
    / "runs"
    / "obb"
    / "aria_objects"
    / "weights"
    / "best.pt",
)
