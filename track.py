import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Eye indices (iris tracking points)
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

cap = cv2.VideoCapture(0)

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def get_iris_center(landmarks, eye_indices, img_w, img_h):
    points = []
    for idx in eye_indices:
        x = int(landmarks.landmark[idx].x * img_w)
        y = int(landmarks.landmark[idx].y * img_h)
        points.append((x, y))
    if points:
        cx = int(np.mean([p[0] for p in points]))
        cy = int(np.mean([p[1] for p in points]))
        return cx, cy
    return None, None

def get_gaze_direction(left_eye_x, right_eye_x, frame_width):
    eye_avg_x = (left_eye_x + right_eye_x) / 2
    if eye_avg_x < frame_width * 0.4:
        return "Looking Left"
    elif eye_avg_x > frame_width * 0.6:
        return "Looking Right"
    else:
        return "Looking Center"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img_h, img_w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            # Get iris centers
            left_eye_x, left_eye_y = get_iris_center(landmarks, LEFT_IRIS, img_w, img_h)
            right_eye_x, right_eye_y = get_iris_center(landmarks, RIGHT_IRIS, img_w, img_h)

            if left_eye_x and right_eye_x:
                # Draw iris positions
                cv2.circle(frame, (left_eye_x, left_eye_y), 3, (0, 255, 0), -1)
                cv2.circle(frame, (right_eye_x, right_eye_y), 3, (0, 255, 0), -1)

                direction = get_gaze_direction(left_eye_x, right_eye_x, img_w)
                cv2.putText(frame, direction, (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    else:
        cv2.putText(frame, "Face Not Detected", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Eye Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
