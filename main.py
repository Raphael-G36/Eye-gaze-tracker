from fastapi import FastAPI, WebSocket
from pathlib import Path
from fastapi.responses import HTMLResponse
from view import EyeTracker
import cv2


app = FastAPI()
eye_tracker = EyeTracker()

@app.get("/")
async def read_root():
    return{"message":"Server is up and running"}

@app.get("/home")
async def home():
    html_file = Path("templates/index.html")
    context = html_file.read_text(encoding="utf-8")
    return HTMLResponse(content=context, status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global cap
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            await websocket.send_json({"error": "Unable to access webcam"})
            break
        result = eye_tracker.process_frame(frame)
        await websocket.send_json(result)
    cap.release()

@app.get("/result")
def results(): 
    cap.release()
    page = Path("templates/result.html")
    context = page.read_text(encoding="utf-8")
    return HTMLResponse(content=context, status_code=200)

           
    
    