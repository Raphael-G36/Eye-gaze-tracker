# from flask import Flask
# import mediapipe as mp 
# import cv2
# import numpy as np

# app = Flask(__name__)

# # Initialize Mediapipe
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# # Define eye landmarks
# LEFT_EYE = [33, 133, 159, 145, 468, 473]  # Includes iris points
# RIGHT_EYE = [362, 263, 386, 374, 469, 474]

# @app.route("/")
# def track_eye_gaze():
#     cap = cv2.VideoCapture(0)
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(rgb_frame)

#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:
#                 # Get landmark positions
#                 height, width, _ = frame.shape
#                 landmarks = {i: (int(face_landmarks.landmark[i].x * width), 
#                                  int(face_landmarks.landmark[i].y * height)) 
#                              for i in LEFT_EYE + RIGHT_EYE}

#                 # Calculate eye width
#                 left_eye_width = abs(landmarks[33][0] - landmarks[133][0])
#                 right_eye_width = abs(landmarks[362][0] - landmarks[263][0])

#                 # Get iris positions
#                 left_iris_x = landmarks[468][0]
#                 right_iris_x = landmarks[469][0]

#                 # Determine gaze direction
#                 if left_iris_x < landmarks[33][0] + 0.3 * left_eye_width:
#                     gaze = "Looking Right"
#                 elif left_iris_x > landmarks[33][0] + 0.7 * left_eye_width:
#                     gaze = "Looking Left"
#                 else:
#                     gaze = "Looking Center"

#                 # Display result
#                 cv2.putText(frame, gaze, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()
    

# app.run(host='127.0.0.1', port='5000' debug=True)

from flask import Flask, Response, render_template
import cv2
import mediapipe as mp

app = Flask(__name__)

# # Initialize Mediapipe
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# # Define eye landmarks
# LEFT_EYE = [33, 133, 159, 145, 468, 473]  # Includes iris points
# RIGHT_EYE = [362, 263, 386, 374, 469, 474]

# def track_eye_gaze():
#     cap = cv2.VideoCapture(0)  # Open webcam
    
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(rgb_frame)

#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:
#                 # Get landmark positions
#                 height, width, _ = frame.shape
#                 landmarks = {i: (int(face_landmarks.landmark[i].x * width), 
#                                  int(face_landmarks.landmark[i].y * height)) 
#                              for i in LEFT_EYE + RIGHT_EYE}

#                 # Calculate eye width
#                 left_eye_width = abs(landmarks[33][0] - landmarks[133][0])
#                 right_eye_width = abs(landmarks[362][0] - landmarks[263][0])

#                 # Get iris positions
#                 left_iris_x = landmarks[468][0]
#                 right_iris_x = landmarks[469][0]

#                 # Determine gaze direction
#                 if left_iris_x < landmarks[33][0] + 0.3 * left_eye_width:
#                     gaze = "Looking Right"
#                 elif left_iris_x > landmarks[33][0] + 0.7 * left_eye_width:
#                     gaze = "Looking Left"
#                 else:
#                     gaze = "Looking Center"

#                 # Display result on video frame
#                 cv2.putText(frame, gaze, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         # Convert frame to JPEG for streaming
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()

@app.route('/')
def index():
    return render_template('index.html')  # Load HTML page


if __name__ == '__main__':
    app.run(debug=True)
