from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import HTMLResponse
from view import EyeTracker
import cv2
import uuid
import datetime
import json
import os
import time


os.makedirs("suspicious_behaviour/image/", exist_ok=True)
os.makedirs("suspicious_behaviour/session_log/", exist_ok=True)

app = FastAPI(title="Eye Tracking Quiz Application")

# CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "Server is up and running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "eye-tracking-quiz"}

@app.get("/home")
async def home():
    html_file = Path("templates/index.html")
    if not html_file.exists():
        return {"error": "Template file not found"}
    context = html_file.read_text(encoding="utf-8")
    session_data['active'] = True
    session_data['session_id'] = str(uuid.uuid4())
    return HTMLResponse(content=context, status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global cap
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            await websocket.send_json({"error": "Unable to access webcam. Please ensure your camera is connected and permissions are granted."})
            await websocket.close()
            return
        
        no_of_images = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                await websocket.send_json({"error": "Unable to read from webcam"})
                break
            result = eye_tracker.process_frame(frame)
            if session_data['active']:
                if result:
                    session_data['data'].append(
                        {"session_id": session_data["session_id"],
                         "timestamp": datetime.datetime.now().isoformat(),
                         "direction": result["direction"],
                         }
                    )
                    if result["direction"] == "Flagged: Looking away for 3+ seconds" and no_of_images < 5:
                        session_id = session_data["session_id"]
                        session_data['data'][-1]["flagged_image"] = f"suspicious_behaviour/image/{session_id}.jpg"
                        cv2.imwrite(f"suspicious_behaviour/image/{session_id}_{int(time.time()*1000)}.jpg", frame)
                        no_of_images += 1
                    else:
                        no_of_images = 0
            await websocket.send_json(result)
    except Exception as e:
        await websocket.send_json({"error": f"An error occurred: {str(e)}"})
    finally:
        if 'cap' in globals() and cap.isOpened():
            cap.release()

def evaluate():
    flagged = 0
    session_data["active"] = False
    filepath = "suspicious_behaviour/session_log/"
    os.makedirs(filepath, exist_ok=True)
    filename = f"session_{session_data['session_id']}.json"
    file = filepath + filename
    with open(file, "w") as f:
        json.dump(session_data["data"], f, indent=2)
        
    with open(file, "r") as f:
        data = json.load(f)
        
        for i in data:
            if i["direction"] == "Flagged: Looking away for 3+ seconds":
                flagged += 1
    
    if flagged > 1000:
        print(f"User with id {session_data['session_id']} engaged in malpractice")
    
    return flagged
        

@app.get("/result")
def results(): 
    global cap
    if 'cap' in globals() and cap.isOpened():
        cap.release()
    evaluate()
    page = Path("templates/result.html")
    if not page.exists():
        return {"error": "Template file not found"}
    context = page.read_text(encoding="utf-8")
    return HTMLResponse(content=context, status_code=200)