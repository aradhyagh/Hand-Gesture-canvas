import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from logic import is_first_finger_up

MODEL_PATH = r"C:\Users\User\Downloads\hand_landmarker.task"

BaseOptions = python.BaseOptions
VisionRunningMode = vision.RunningMode

options = vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)

# Webcam loop

cap = cv2.VideoCapture(0)
timestamp = 0

canvas = None
prev_point = None

print("Running... Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if canvas is None:
        canvas = np.zeros_like(frame)  # solid drawing canvas (black background, but we mask it)

    timestamp += 15
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    result = detector.detect_for_video(mp_image, timestamp)

    h, w, _ = frame.shape
    kpts = []

    if result.hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(result.hand_landmarks):
            for lm in hand_landmarks:
                px = int(lm.x * w)
                py = int(lm.y * h)
                kpts.append((hand_idx, (px, py)))

    # DRAWING LOGIC (index finger)
    if is_first_finger_up(kpts):
        if len(kpts) >= 9 and kpts[8][0] == 0:  # landmark 8 = index finger tip
            x, y = kpts[8][1]

            if prev_point is None:
                prev_point = (x, y)

            # draw solid line on canvas
            cv2.line(canvas, prev_point, (x, y), (0, 0, 255), 6)  # pure green, solid
            prev_point = (x, y)
    else:
        prev_point = None

    # MERGE CANVAS → FRAME (NO transparency)
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)

    frame[mask == 255] = canvas[mask == 255]

    # Debug keypoints
    for hand, kpt in kpts:
        cv2.circle(frame, kpt, 3, (255, 0, 0), cv2.FILLED)

    # TOP TEXT (Blue with Black Border)
    text = "Finger Canvas"
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.2

    frame = cv2.flip(frame, 1)
    cv2.putText(frame, text, (20, 40), font, scale, (0, 0, 0), 5, cv2.LINE_AA)  # border
    cv2.putText(frame, text, (20, 40), font, scale, (255, 0, 0), 2, cv2.LINE_AA)  # blue text

    cv2.imshow("Hand Drawing", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

