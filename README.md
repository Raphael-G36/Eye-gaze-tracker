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
- **Frontend**: Vanilla HTML/CSS/JavaScript - Deployed separately on Vercel
- **Eye Tracking**: MediaPipe Face Mesh for real-time gaze detection
- **Deployment**: 
  - Frontend: Vercel
  - Backend: Railway

## 📋 Prerequisites

- Python 3.12+
- Webcam/Camera access
- Node.js (for local frontend testing, optional)

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

### Frontend Setup (Local Testing)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Update the backend URL in `config.js`**
   ```javascript
   const BACKEND_CONFIG = {
       url: 'ws://localhost:8000' // For local development
   };
   ```

3. **Serve the frontend** (using any static file server)
   ```bash
   # Using Python
   python -m http.server 3000
   
   # Or using Node.js http-server
   npx http-server -p 3000
   ```

4. **Open in browser**
   Navigate to `http://localhost:3000`

## 🌐 Deployment Guide

### Backend Deployment on Railway

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

4. **Set environment variables** (if needed)
   - Go to your project settings
   - Add any required environment variables

5. **Deploy**
   - Railway will automatically build and deploy
   - Note your deployment URL (e.g., `your-app.railway.app`)

6. **Update CORS settings**
   - In `main.py`, update the `allow_origins` in CORS middleware with your Vercel domain:
   ```python
   allow_origins=["https://your-vercel-app.vercel.app"]
   ```

### Frontend Deployment on Vercel

1. **Create a Vercel account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up or log in

2. **Install Vercel CLI** (optional, can use web interface)
   ```bash
   npm i -g vercel
   ```

3. **Deploy from frontend directory**
   ```bash
   cd frontend
   vercel
   ```
   Or use the Vercel web interface:
   - Click "New Project"
   - Import your repository
   - Set root directory to `frontend`
   - Deploy

4. **Configure environment variables**
   - In Vercel dashboard, go to your project settings
   - Add environment variable:
     - Key: `VITE_BACKEND_URL`
     - Value: `wss://your-railway-app.railway.app` (your Railway backend URL)

5. **Update config.js**
   - Edit `frontend/config.js` with your Railway backend URL:
   ```javascript
   const BACKEND_CONFIG = {
       url: 'wss://your-railway-app.railway.app'
   };
   ```

6. **Redeploy** (if needed)
   - Vercel will automatically redeploy on git push
   - Or manually trigger a redeploy from the dashboard

## 📖 How to Use

### For Testers/Users

1. **Access the Application**
   - Open the deployed frontend URL (Vercel)
   - Or open `http://localhost:3000` for local testing

2. **Grant Camera Permissions**
   - When prompted, allow camera access
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

- **Backend URL**: Set in `frontend/config.js` or via `VITE_BACKEND_URL` environment variable
- **WebSocket URL**: Automatically constructed from backend URL

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
├── templates/             # Backend HTML templates
│   ├── index.html
│   └── result.html
├── frontend/              # Frontend for Vercel deployment
│   ├── index.html
│   ├── result.html
│   ├── config.js          # Backend URL configuration
│   └── vercel.json        # Vercel deployment configuration
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
  - WebSocket API - Real-time eye tracking updates

- **Deployment**:
  - Railway - Backend hosting
  - Vercel - Frontend hosting

## 🐛 Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Ensure no other application is using the camera
- Try refreshing the page and granting permissions again

### WebSocket Connection Failed
- Verify the backend URL in `config.js` is correct
- Check that Railway backend is running and accessible
- Ensure CORS is properly configured in `main.py`

### Face Not Detected
- Improve lighting conditions
- Position yourself directly facing the camera
- Ensure your face is fully visible
- Check camera focus and quality

### Deployment Issues
- Verify all environment variables are set correctly
- Check Railway logs for backend errors
- Verify Vercel build logs for frontend issues
- Ensure `Procfile` and `railway.json` are in the root directory

## 📝 Notes

- **Webcam Requirement**: This application requires webcam access. It won't work on devices without cameras.
- **HTTPS/WSS**: Production deployments require HTTPS (Vercel) and WSS (Railway) for WebSocket connections.
- **Privacy**: All eye tracking data is logged locally on the server. Consider privacy implications before deploying.

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

