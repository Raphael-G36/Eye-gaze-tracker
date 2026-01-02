# 👁️ Eye Tracking Quiz Application

An intelligent online assessment platform that monitors eye gaze using MediaPipe to ensure academic integrity during quizzes. The application tracks eye movements and flags suspicious behavior when users look away from the screen for extended periods.

## ✨ Features

- **Real-time Eye Tracking**: Uses MediaPipe Face Mesh to track eye gaze direction
- **Suspicious Behavior Detection**: Flags users who look away for 3+ seconds
- **Interactive Quiz Interface**: Modern, responsive UI with 10 quiz questions
- **Timer-based Assessment**: 120-second time limit for quiz completion
- **Session Logging**: Records all eye tracking data and flagged events
- **Beautiful UI**: Modern gradient design with smooth animations

## 🏗️ Architecture

- **Backend**: FastAPI (Python) - Handles WebSocket connections and eye tracking processing
- **Frontend**: Vanilla HTML/CSS/JavaScript - Served by FastAPI backend
- **Eye Tracking**: MediaPipe Face Mesh for real-time gaze detection
- **Camera Capture**: Browser-based (MediaDevices API) - Frames sent to backend via WebSocket
- **Deployment**: Railway (single deployment, no separate frontend needed)

## 📋 Prerequisites

- Python 3.12+
- Webcam/Camera access (for users taking the quiz)
- Modern web browser with camera support

## 🚀 Local Development Setup

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The backend will be available at `http://localhost:8000`

### Access the Application

1. **Open in browser**
   Navigate to `http://localhost:8000`
   
2. **Landing Page**
   - You'll see the landing page at the root URL
   - Click "Show Demo" to access the quiz

3. **Start Quiz**
   - Click "Start Quiz" button
   - Grant camera permissions when prompted
   - The browser will capture video from your camera

## 🌐 Deployment Guide

### Deploy to Railway (Single Deployment)

The application is now fully deployable on Railway with frontend camera capture. No separate frontend deployment needed!

1. **Create a Railway account**
   - Go to [railway.app](https://railway.app)
   - Sign up or log in

2. **Create a new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo" (recommended) or "Empty Project"

3. **Configure the project**
   - If deploying from GitHub, connect your repository
   - Railway will automatically detect the Python project
   - The `Procfile` and `railway.json` will configure the deployment

4. **Deploy**
   - Railway will automatically build and deploy
   - Note your deployment URL (e.g., `your-app.railway.app`)

5. **Access your application**
   - Visit `https://your-app.railway.app`
   - The landing page will be at the root URL
   - Click "Show Demo" to access the quiz

### How It Works on Railway

✅ **Works perfectly on Railway!** The camera is accessed from the user's browser, not the server:
- Browser captures video using MediaDevices API
- Frames are sent to Railway backend via WebSocket
- Backend processes frames with MediaPipe
- Results sent back to browser
- No server camera needed!

### CORS Configuration

The app is configured to accept connections from any origin. If you need to restrict access:

1. Edit `main.py`
2. Update the `allow_origins` in CORS middleware:
   ```python
   allow_origins=["https://your-domain.com"]
   ```
3. Commit and push (Railway auto-deploys)

## 📖 How to Use

### For Testers/Users

1. **Access the Application**
   - Open the deployed Railway URL (e.g., `https://your-app.railway.app`)
   - Or open `http://localhost:8000` for local testing

2. **Grant Camera Permissions**
   - When prompted, allow camera access
   - The browser will capture video from your camera
   - Ensure your webcam is connected and working

3. **Position Yourself**
   - Sit in a well-lit area
   - Face the camera directly
   - Keep your face centered in the frame

4. **Start the Quiz**
   - Click "Start Quiz" button
   - Wait for eye tracking to initialize
   - The gaze direction indicator will show your current status

5. **Take the Quiz**
   - Answer questions by clicking on your chosen option
   - Keep your eyes on the screen
   - You have 120 seconds to complete all questions
   - Looking away for 3+ seconds will be flagged

6. **Complete the Quiz**
   - Click "End Quiz" when finished
   - Or wait for the timer to expire
   - View your results on the results page

### Important Guidelines

- ✅ Ensure good lighting for accurate face detection
- ✅ Keep your face visible and centered
- ✅ Maintain eye contact with the screen
- ✅ Avoid looking away for extended periods
- ✅ Answer questions within the time limit
- ❌ Don't block your face or camera
- ❌ Don't look away for more than 3 seconds

## 🔧 Configuration

### Backend Configuration

- **Port**: Set via `PORT` environment variable (Railway sets this automatically)
- **CORS**: Configure allowed origins in `main.py`
- **Session Logs**: Stored in `suspicious_behaviour/session_log/`
- **Flagged Images**: Stored in `suspicious_behaviour/image/`

### Frontend Configuration

- **WebSocket URL**: Automatically detected (localhost for local dev, Railway URL for production)
- **Camera Capture**: Browser-based using MediaDevices API
- **Frame Rate**: ~10 FPS (every 100ms) to optimize bandwidth

## 📁 Project Structure

```
tracker/
├── main.py                 # FastAPI backend application
├── view.py                 # EyeTracker class with MediaPipe integration
├── track.py                # Legacy tracking code (not used)
├── requirements.txt        # Python dependencies
├── Procfile               # Railway deployment configuration
├── railway.json           # Railway project configuration
├── runtime.txt            # Python version specification
├── templates/             # HTML templates (served by FastAPI)
│   ├── landing.html       # Landing page
│   ├── index.html         # Quiz page (with frontend camera capture)
│   └── result.html        # Results page
├── suspicious_behaviour/  # Generated data
│   ├── image/            # Flagged behavior screenshots
│   └── session_log/      # Session data logs
└── README.md             # This file
```

## 🛠️ Technologies Used

- **Backend**:
  - FastAPI - Modern Python web framework
  - WebSockets - Real-time communication
  - MediaPipe - Face mesh and eye tracking
  - OpenCV - Video processing

- **Frontend**:
  - HTML5/CSS3 - Modern responsive design
  - JavaScript - Interactive quiz logic
  - MediaDevices API - Browser camera capture
  - WebSocket API - Real-time eye tracking updates
  - Canvas API - Frame capture and encoding

- **Deployment**:
  - Railway - Full-stack hosting (backend + frontend)

## 🐛 Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Ensure no other application is using the camera
- Try refreshing the page and granting permissions again
- **Note**: Camera is accessed from your browser, not the server
- Works on Railway because camera is client-side!

### WebSocket Connection Failed
- Check that Railway backend is running and accessible
- Ensure CORS is properly configured in `main.py`
- Verify WebSocket URL is using `wss://` (secure) for production
- Check browser console for connection errors

### Face Not Detected
- Improve lighting conditions
- Position yourself directly facing the camera
- Ensure your face is fully visible
- Check camera focus and quality

### Deployment Issues
- Check Railway logs for backend errors
- Ensure `Procfile` and `railway.json` are in the root directory
- Verify all dependencies in `requirements.txt` are correct
- Check that OpenCV/MediaPipe dependencies install correctly

## 📝 Notes

- **Webcam Requirement**: This application requires webcam access. It won't work on devices without cameras.
- **Browser-Based Camera**: Camera is accessed from the user's browser, not the server. This means:
  - ✅ Works on Railway (no server camera needed)
  - ✅ Works on any hosting platform
  - ✅ Better privacy (camera stays in browser)
  - ✅ Cross-platform compatibility
- **HTTPS/WSS**: Production deployments require HTTPS and WSS for WebSocket connections (Railway provides this automatically).
- **Privacy**: All eye tracking data is logged on the server. Consider privacy implications before deploying.
- **Frame Rate**: Frames are sent at ~10 FPS to optimize bandwidth while maintaining accuracy.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- MediaPipe team for the excellent face mesh solution
- FastAPI for the robust web framework
- Railway and Vercel for hosting platforms

---

**Made with ❤️ for academic integrity in online assessments**

