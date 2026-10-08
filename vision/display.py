import cv2
 
 
def draw_text(img, text, org, color=(0, 255, 255)):
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 1)
 
 
def draw_frame(frame, s):
    """Return a copy of `frame` with boxes, status, what ARIA heard, and a mic level bar."""
    view = frame.copy()              # draw on a copy; the detector reads the original
    h = view.shape[0]
    det = s.detector
 
    for x1, y1, x2, y2, label in det.boxes:
        cv2.rectangle(view, (x1, y1), (x2, y2), (0, 255, 0), 2)
        draw_text(view, label, (x1, max(y1 - 8, 20)), (0, 255, 0))
 
    status = ("YOLO ERROR - see terminal" if det.error
              else "loading vision..." if not det.ready
              else s.status)
    draw_text(view, status, (15, 30))
    if s.heard:
        draw_text(view, "You: " + s.heard[:80], (15, 62), (255, 255, 255))
 
    # mic level bar: the red tick is the speech threshold; the bar should pass it when you talk
    level, threshold = (s.mic.level, s.mic.threshold) if s.mic else (0.0, 1e9)
    fill = int(300 * min(level / max(threshold * 3, 1), 1.0))
    cv2.rectangle(view, (15, h - 35), (315, h - 15), (255, 255, 255), 1)
    cv2.rectangle(view, (15, h - 35), (15 + fill, h - 15),
                  (0, 255, 0) if level > threshold else (160, 160, 160), -1)
    cv2.line(view, (115, h - 40), (115, h - 10), (0, 0, 255), 2)
    return view
 