import cv2, time

for i in (0, 1):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    print(f"camera {i}: opened = {cap.isOpened()}")
    if not cap.isOpened():
        continue
    time.sleep(1.0)                      # warm-up
    bad = 0
    while bad < 60:
        ok, frame = cap.read()
        if not ok:
            bad += 1
            time.sleep(0.05)
            continue
        bad = 0
        print(f"camera {i}: frame {frame.shape}, mean color diff "
              f"{abs(frame[...,0].astype(int)-frame[...,2].astype(int)).mean():.1f}", end="\r")
        cv2.imshow(f"camera {i} - press q for next", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    print()