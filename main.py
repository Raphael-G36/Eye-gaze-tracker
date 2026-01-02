from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import HTMLResponse
import uuid
import datetime
import json
import os
import time
import asyncio

# Lazy import of OpenCV and EyeTracker to avoid startup errors on Railway
# Railway servers don't have cameras, so we make these optional
try:
    import cv2
    from view import EyeTracker
    EYE_TRACKING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Eye tracking not available: {e}")
    EYE_TRACKING_AVAILABLE = False
    cv2 = None
    EyeTracker = None


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

# Initialize EyeTracker lazily to avoid import errors during startup
eye_tracker = None

def get_eye_tracker():
    global eye_tracker
    if not EYE_TRACKING_AVAILABLE:
        raise RuntimeError("Eye tracking is not available on this server. Railway servers don't have camera access.")
    if eye_tracker is None:
        eye_tracker = EyeTracker()
    return eye_tracker

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
    if not EYE_TRACKING_AVAILABLE or cv2 is None:
        return None, None
    
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
    if not EYE_TRACKING_AVAILABLE:
        return {
            "status": "error",
            "message": "Eye tracking not available",
            "note": "OpenCV/MediaPipe not available on this server. Railway servers don't have camera access.",
            "suggestions": [
                "Run the application locally for camera functionality",
                "Railway servers are headless and don't support camera access"
            ]
        }
    
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
    connection_active = True
    
    try:
        # Send initial connection message
        try:
            await websocket.send_json({"direction": "Waiting for camera feed..."})
        except Exception as e:
            print(f"Failed to send initial message: {e}")
            return
        
        print("WebSocket connected, waiting for frames from frontend...")
        
        # Check if OpenCV and MediaPipe are available
        if not EYE_TRACKING_AVAILABLE or cv2 is None:
            await websocket.send_json({
                "error": "⚠️ Eye tracking unavailable - OpenCV/MediaPipe not available. Quiz will continue without monitoring.",
                "warning": True,
                "direction": "Eye tracking disabled"
            })
            # Keep connection alive
            try:
                while connection_active:
                    await asyncio.sleep(5)
                    try:
                        await websocket.send_json({
                            "direction": "Eye tracking disabled",
                            "warning": True
                        })
                    except:
                        break
            except:
                pass
            return
        
        # Get eye tracker
        tracker = get_eye_tracker()
        
        frame_count = 0
        consecutive_errors = 0
        max_errors = 10
        
        # Main processing loop - receive frames from frontend
        print("Starting frame processing loop (receiving from frontend)...")
        while connection_active:
            try:
                # Receive message from frontend
                message = await websocket.receive_text()
                data = json.loads(message)
                
                if data.get("type") == "frame":
                    # Decode base64 image
                    import base64
                    image_data = data["data"]
                    # Remove data URL prefix if present
                    if "," in image_data:
                        image_data = image_data.split(",")[1]
                    
                    # Decode base64 to bytes
                    frame_bytes = base64.b64decode(image_data)
                    
                    # Convert bytes to numpy array
                    import numpy as np
                    nparr = np.frombuffer(frame_bytes, np.uint8)
                    
                    # Decode image using OpenCV
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if frame is None:
                        consecutive_errors += 1
                        if consecutive_errors >= max_errors:
                            await websocket.send_json({"error": "Failed to decode frames"})
                            break
                        continue
                    
                    # Reset error counter on success
                    consecutive_errors = 0
                    frame_count += 1
                    
                    # Process every 3rd frame to reduce load (~3-4 FPS processing)
                    if frame_count % 3 == 0:
                        try:
                            # Process frame with eye tracker
                            result = tracker.process_frame(frame)
                            
                            # Log to session data if active
                            if session_data['active'] and result and "direction" in result:
                                session_data['data'].append({
                                    "session_id": session_data["session_id"],
                                    "timestamp": datetime.datetime.now().isoformat(),
                                    "direction": result["direction"],
                                })
                                
                                # Save flagged images
                                if result["direction"] == "Flagged: Looking away for 3+ seconds":
                                    session_id = session_data["session_id"]
                                    try:
                                        cv2.imwrite(f"suspicious_behaviour/image/{session_id}_{int(time.time()*1000)}.jpg", frame)
                                    except:
                                        pass
                            
                            # Send result back to frontend
                            await websocket.send_json(result)
                            
                        except Exception as e:
                            print(f"Error processing frame: {e}")
                            import traceback
                            traceback.print_exc()
                            consecutive_errors += 1
                            if consecutive_errors >= max_errors:
                                break
                    
                elif data.get("type") == "ping":
                    # Respond to ping to keep connection alive
                    await websocket.send_json({"type": "pong"})
                    
            except asyncio.CancelledError:
                print("WebSocket task cancelled")
                connection_active = False
                break
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    break
            except Exception as e:
                print(f"Unexpected error in frame loop: {e}")
                import traceback
                traceback.print_exc()
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    break
                await asyncio.sleep(0.1)
                
                # Process frame directly (MediaPipe is fast enough)
                try:
                    tracker = get_eye_tracker()
                    result = tracker.process_frame(frame)
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
        # Clean up
        connection_active = False
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