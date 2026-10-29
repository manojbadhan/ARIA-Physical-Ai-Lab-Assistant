
from pathlib import Path
from ultralytics import YOLO

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent


DATA_YAML = (
    SCRIPT_DIR
    / "aria_combined_all_obb_dataset"
    / "data.yaml"
)

# Start from pretrained OBB weights
MODEL = "yolov8s-obb.pt"

# Training settings
EPOCHS = 100
IMAGE_SIZE = 640
BATCH_SIZE = 4

def main():
    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"Dataset YAML not found: {DATA_YAML}"
        )

    model = YOLO(MODEL)

    model.train(
        data=str(DATA_YAML),
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        device=0,
        workers=2,
        patience=20,
        project=str(SCRIPT_DIR / "runs" / "obb"),
        name="aria_combined_13_classes",
        pretrained=True,
        plots=True,
        save=True,
        seed=42
    )

if __name__ == "__main__":
    main()
