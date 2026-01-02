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
import asyncio


os.makedirs("suspicious_behaviour/image/", exist_ok=True)
os.makedirs("suspicious_behaviour/session_log/", exist_ok=True)

app = FastAPI(title="Eye Tracking Quiz Application")

# CORS configuration for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
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

def find_available_camera():
    """Try to find an available camera by testing different indices"""
    print("Starting camera search...")
    # On Windows, try DirectShow backend first (more reliable)
    backends = []
    if os.name == 'nt':  # Windows
        backends = [cv2.CAP_DSHOW, cv2.CAP_ANY]
    else:
        backends = [cv2.CAP_ANY]
    
    for backend in backends:
        backend_name = "DirectShow" if backend == cv2.CAP_DSHOW else "Default"
        print(f"Trying {backend_name} backend...")
        for camera_index in range(3):  # Try cameras 0, 1, 2
            cap = None
            try:
                print(f"  Attempting camera index {camera_index}...")
                # Try to open camera
                cap = cv2.VideoCapture(camera_index, backend)
                
                if not cap.isOpened():
                    print(f"    Camera {camera_index} failed to open")
                    continue
                
                print(f"    Camera {camera_index} opened, testing frame read...")
                
                # Try to read a frame to verify it works
                # Read a few frames to let camera initialize (some cameras need warm-up)
                for attempt in range(5):
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        height, width = frame.shape[:2]
                        print(f"    ✓ Success! Camera {camera_index} working - Frame size: {width}x{height}")
                        return cap, camera_index
                    time.sleep(0.1)  # Small delay between attempts
                
                # If we got here, camera opened but can't read frames
                print(f"    Camera {camera_index} opened but cannot read frames")
                cap.release()
                cap = None
                
            except Exception as e:
                print(f"    Error testing camera {camera_index}: {e}")
                if cap is not None:
                    try:
                        cap.release()
                    except:
                        pass
                cap = None
    
    print("No working camera found!")
    return None, None

@app.get("/")
async def read_root():
    """Landing page"""
    html_file = Path("templates/landing.html")
    if not html_file.exists():
        return {"message": "Server is up and running", "status": "healthy", "note": "Landing page not found"}
    context = html_file.read_text(encoding="utf-8")
    return HTMLResponse(content=context, status_code=200)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "eye-tracking-quiz"}

@app.get("/test-camera")
async def test_camera():
    """Test endpoint to check camera availability"""
    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    cap, camera_index = await loop.run_in_executor(None, find_available_camera)
    if cap is None:
        return {
            "status": "error",
            "message": "No camera found",
            "suggestions": [
                "Check if camera is connected",
                "Close other applications using the camera",
                "Check camera permissions",
                "Try restarting the application"
            ]
        }
    
    # Try to read a frame
    ret, frame = cap.read()
    cap.release()
    
    if ret and frame is not None:
        height, width = frame.shape[:2]
        return {
            "status": "success",
            "camera_index": camera_index,
            "frame_size": f"{width}x{height}",
            "message": "Camera is working correctly"
        }
    else:
        return {
            "status": "error",
            "message": "Camera opened but cannot read frames"
        }

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
    cap = None
    connection_active = True
    
    try:
        # Send initial connection message
        try:
            await websocket.send_json({"direction": "Initializing camera..."})
        except Exception as e:
            print(f"Failed to send initial message: {e}")
            return
        
        print("WebSocket connected, opening camera...")
        
        # Try to open camera directly (simpler approach)
        # On Windows, use DirectShow backend which is more reliable
        backend = cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_ANY
        
        # Try camera indices 0, 1, 2
        camera_found = False
        for camera_index in range(3):
            try:
                print(f"Trying camera index {camera_index}...")
                cap = cv2.VideoCapture(camera_index, backend)
                
                if cap.isOpened():
                    # Try to read a frame to verify it works
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"✓ Camera {camera_index} working! Frame size: {frame.shape}")
                        camera_found = True
                        break
                    else:
                        print(f"Camera {camera_index} opened but can't read frames")
                        cap.release()
                        cap = None
                else:
                    print(f"Camera {camera_index} failed to open")
                    if cap:
                        cap.release()
                    cap = None
            except Exception as e:
                print(f"Error with camera {camera_index}: {e}")
                import traceback
                traceback.print_exc()
                if cap:
                    try:
                        cap.release()
                    except:
                        pass
                cap = None
        
        if not camera_found or cap is None or not cap.isOpened():
            print("No working camera found")
            error_msg = "Unable to access webcam. Please ensure:\n"
            error_msg += "1. Your camera is connected and working\n"
            error_msg += "2. No other application is using the camera (Zoom, Teams, etc.)\n"
            error_msg += "3. Camera permissions are granted in Windows Settings\n"
            error_msg += "4. Try closing all apps and restarting this application"
            try:
                await websocket.send_json({"error": error_msg})
                await websocket.close(code=1000)  # Normal closure
            except:
                pass
            return
        
        print("Camera successfully opened!")
        
        # Set camera properties for better performance
        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 30)
        except:
            pass  # Some cameras don't support these settings
        
        # Send initial connection message
        try:
            await websocket.send_json({"direction": "Camera ready! Detecting face..."})
        except Exception as e:
            print(f"Failed to send ready message: {e}")
            if cap:
                cap.release()
            return
        
        # Give camera a moment to warm up
        await asyncio.sleep(0.3)
        
        no_of_images = 0
        frame_count = 0
        consecutive_errors = 0
        max_errors = 10
        
        # Main processing loop
        print("Starting frame processing loop...")
        while connection_active:
            try:
                
                # Check if cap is still valid
                if cap is None or not cap.isOpened():
                    print("Camera is no longer open, exiting loop")
                    try:
                        await websocket.send_json({"error": "Camera connection lost"})
                    except:
                        pass
                    break
                
                # Read frame from camera
                ret, frame = cap.read()
                if not ret or frame is None:
                    consecutive_errors += 1
                    print(f"Failed to read frame from camera (error {consecutive_errors}/{max_errors})")
                    if consecutive_errors >= max_errors:
                        try:
                            await websocket.send_json({"error": "Unable to read from webcam after multiple attempts"})
                        except:
                            pass
                        break
                    await asyncio.sleep(0.1)
                    continue
                
                # Reset error counter on success
                consecutive_errors = 0
                
                # Process frame directly (MediaPipe is fast enough)
                try:
                    result = eye_tracker.process_frame(frame)
                except Exception as process_error:
                    print(f"Error processing frame: {process_error}")
                    result = {"direction": "Processing error"}
                
                # Ensure result is always a dictionary
                if result is None:
                    result = {"direction": "Processing..."}
                
                # Only send updates every few frames to reduce WebSocket traffic
                # Send every 3rd frame (roughly 10 FPS instead of 30)
                if frame_count % 3 == 0:
                    try:
                        if session_data['active']:
                            if result and "direction" in result:
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
                        
                        # Send result to client
                        await websocket.send_json(result)
                    except Exception as send_error:
                        # WebSocket might be closed
                        print(f"Error sending to WebSocket: {send_error}")
                        connection_active = False
                        break
                
                frame_count += 1
                
                # Small delay to prevent overwhelming the system
                await asyncio.sleep(0.033)  # ~30 FPS
                
            except asyncio.CancelledError:
                print("WebSocket task cancelled")
                connection_active = False
                break
            except Exception as frame_error:
                print(f"Unexpected error in frame loop: {frame_error}")
                import traceback
                traceback.print_exc()
                try:
                    await websocket.send_json({"error": f"Frame processing error: {str(frame_error)}"})
                except:
                    pass
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    break
                await asyncio.sleep(0.1)
                
    except asyncio.CancelledError:
        print("WebSocket connection cancelled")
    except Exception as e:
        print(f"Error in WebSocket handler: {e}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.send_json({"error": f"An error occurred: {str(e)}"})
            await websocket.close(code=1011)  # Internal error
        except:
            pass
    finally:
        # Always release camera when done
        connection_active = False
        if cap is not None:
            try:
                if cap.isOpened():
                    cap.release()
                    print("Camera released")
            except Exception as e:
                print(f"Error releasing camera: {e}")
        try:
            cv2.destroyAllWindows()
        except:
            pass
        print("WebSocket connection closed")

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
    # Camera is managed per WebSocket connection, not globally
    evaluate()
    page = Path("templates/result.html")
    if not page.exists():
        return {"error": "Template file not found"}
    context = page.read_text(encoding="utf-8")
    return HTMLResponse(content=context, status_code=200)