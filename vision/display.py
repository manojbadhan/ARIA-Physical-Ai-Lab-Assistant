
import cv2
import numpy as np


def draw_text(img, text, org, color=(0, 255, 255)):
    cv2.putText(
        img, text, org, cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 0, 0), 4
    )
    cv2.putText(
        img, text, org, cv2.FONT_HERSHEY_SIMPLEX,
        0.7, color, 1
    )


def draw_frame(frame, s):
    """Draw OBB detections, status, speech text, and microphone level."""
    view = frame.copy()
    h, w = view.shape[:2]
    det = s.detector

    # Draw oriented bounding boxes from the trained OBB model.
    polygons = getattr(det, "obb_polygons", [])

    if polygons:
        for item in polygons:
            points = np.asarray(item["points"], dtype=np.int32).reshape(-1, 1, 2)
            label = item["label"]
            confidence = item.get("confidence")

            cv2.polylines(
                view, [points], True, (0, 255, 0), 2
            )

            x1 = int(points[:, 0, 0].min())
            y1 = int(points[:, 0, 1].min())

            text = (
                f"{label} {confidence:.2f}"
                if confidence is not None
                else label
            )

            draw_text(
                view,
                text,
                (max(5, x1), max(20, y1 - 8)),
                (0, 255, 0),
            )

    else:
        # Fallback for older detectors that provide ordinary rectangles.
        for x1, y1, x2, y2, label in getattr(det, "boxes", []):
            cv2.rectangle(
                view, (int(x1), int(y1)),
                (int(x2), int(y2)), (0, 255, 0), 2
            )
            draw_text(
                view, label,
                (int(x1), max(int(y1) - 8, 20)),
                (0, 255, 0),
            )

    status = (
        "YOLO ERROR - see terminal" if det.error
        else "loading vision..." if not det.ready
        else s.status
    )
    draw_text(view, status, (15, 30))

    if s.heard:
        draw_text(view, "You: " + s.heard[:80], (15, 62), (255, 255, 255))

    # Microphone level bar
    level, threshold = (
        (s.mic.level, s.mic.threshold)
        if s.mic else (0.0, 1e9)
    )

    fill = int(300 * min(level / max(threshold * 3, 1), 1.0))

    cv2.rectangle(
        view, (15, h - 35), (315, h - 15),
        (255, 255, 255), 1
    )
    cv2.rectangle(
        view, (15, h - 35), (15 + fill, h - 15),
        (0, 255, 0) if level > threshold else (160, 160, 160), -1
    )
    cv2.line(
        view, (115, h - 40), (115, h - 10),
        (0, 0, 255), 2
    )

    return view
