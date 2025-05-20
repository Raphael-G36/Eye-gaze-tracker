from fastapi import FastAPI, WebSocket
from pathlib import Path
from fastapi.responses import HTMLResponse
from view import EyeTracker
import cv2
import uuid
import datetime
import json




app = FastAPI()
eye_tracker = EyeTracker()

session_data ={
    "active":False,
    "session_id": None,
    "data":[]
}

flagged = 0
looking_left = 0
looking_right = 0

@app.get("/")
async def read_root():
    return{"message":"Server is up and running"}

@app.get("/home")
async def home():
    html_file = Path("templates/index.html")
    context = html_file.read_text(encoding="utf-8")
    session_data['active']= True
    session_data['session_id'] = str(uuid.uuid4())
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
        if session_data['active']:
            if result:
                session_data['data'].append(
                    {"session_id" : session_data["session_id"],
                     "timestamp" : datetime.datetime.now().isoformat(),
                     "direction" : result["direction"],
                     }
                )
            else:
                await websocket.send_json({"error": "No face detected"})
        await websocket.send_json(result)
    cap.release()

def evaluate():
    flagged = 0
    session_data["active"] = False
    filepath = "session_log/"
    filename = f"session_{session_data["session_id"]}.json"
    file = filepath + filename
    with open(file, "w") as f:
        json.dump(session_data["data"], f, indent=2)
        
    with open(file, "r") as f:
        data = json.load(f)
        
        for i in data:
            if i["direction"] == "Flagged: Looking away for 3+ seconds":
                flagged += 1
    
    if flagged > 1000:
        print(f"User with id {i['session_id']} engaged in malpractice")
        

@app.get("/result")
def results(): 
    if cap.isOpened():
        cap.release()
        evaluate()
    page = Path("templates/result.html")
    context = page.read_text(encoding="utf-8")
    return HTMLResponse(content=context, status_code=200)
    




        
    
    