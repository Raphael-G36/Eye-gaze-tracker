from fastapi import FastAPI, WebSocket
from view import EyeTracker
import cv2


app = FastAPI()
eye_tracker = EyeTracker()


@app.get("/")
def read_root():
    return {"message": "welcome to fast api"}

@app.post("/process_frame")
def process_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        return {"error": "unable to access camera"}
    result = eye_tracker.process_frame(frame)
    cap.release()
    return {"message": "frame processed"}, cv2.putText(frame, result["direction"], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            await websocket.send_json({"error": "Unable to access webcam"})
            break
        result = eye_tracker.process_frame(frame)
        await websocket.send_json(result)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    await websocket.close()