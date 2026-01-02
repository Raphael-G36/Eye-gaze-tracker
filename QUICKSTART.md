# ⚡ Quick Start Guide

Get your Eye Tracking Quiz Application up and running in minutes!

## 🏃 Local Development (5 minutes)

### Backend

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Update config.js with local backend
# Change: url: 'ws://localhost:8000'

# 3. Serve the frontend (choose one)
python -m http.server 3000
# OR
npx http-server -p 3000
```

### Test

1. Open `http://localhost:3000`
2. Click "Start Quiz"
3. Grant camera permissions
4. Take the quiz!

## 🚀 Production Deployment (15 minutes)

### Backend → Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. New Project → Deploy from GitHub
4. Select your repo
5. **Note your Railway URL** (e.g., `your-app.railway.app`)

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com)
2. New Project → Import GitHub repo
3. **Set Root Directory to `frontend`**
4. Add Environment Variable:
   - Key: `VITE_BACKEND_URL`
   - Value: `wss://your-railway-app.railway.app`
5. Update `frontend/config.js` with Railway URL
6. Deploy!

### Configure CORS

1. Edit `main.py`
2. Update `allow_origins` with your Vercel URL
3. Commit and push (Railway auto-deploys)

## ✅ Checklist

- [ ] Backend running locally
- [ ] Frontend running locally
- [ ] Camera permissions working
- [ ] Quiz completes successfully
- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] CORS configured
- [ ] Production URL tested

## 🆘 Common Issues

**Camera not working?**

- Use HTTPS (required in production)
- Grant browser permissions
- Check camera isn't used by another app

**WebSocket fails?**

- Verify Railway URL in `config.js`
- Check CORS settings in `main.py`
- Ensure backend is running

**Need more help?**

- See [README.md](README.md) for detailed docs
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guide

---

**Ready to deploy?** Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide for step-by-step instructions!
