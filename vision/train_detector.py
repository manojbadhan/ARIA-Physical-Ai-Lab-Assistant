from pathlib import Path
from ultralytics import YOLO

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_YAML = Path(__file__).resolve().parent / "aria_dataset.yaml"
MODEL_PATH = PROJECT_ROOT / "yolo11s.pt"

if not DATA_YAML.exists():
    raise FileNotFoundError(f"Dataset config not found: {DATA_YAML}")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"YOLO model not found: {MODEL_PATH}")

print("Loading pretrained YOLO11 model...")
model = YOLO(str(MODEL_PATH))

print("Starting baseline training...")
model.train(
    data=str(DATA_YAML),
    epochs=30,
    imgsz=640,
    batch=8,
    workers=0,
    project=str(PROJECT_ROOT / "runs" / "detect"),
    name="aria_baseline",
    exist_ok=True,
)

print("Training finished!")
print(
    "Best model:",
    PROJECT_ROOT / "runs" / "detect" / "aria_baseline" / "weights" / "best.pt",
)