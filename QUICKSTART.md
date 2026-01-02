# ⚡ Quick Start Guide

Get your Eye Tracking Quiz Application up and running in minutes!

## 🏃 Local Development (5 minutes)

### Setup and Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --reload --port 8000
```

### Test

1. Open `http://localhost:8000`
2. Click "Show Demo" or "Start Quiz"
3. Grant camera permissions
4. Take the quiz!

## 🚀 Production Deployment (15 minutes)

### Deploy to Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. New Project → Deploy from GitHub
4. Select your repo
5. **Note your Railway URL** (e.g., `your-app.railway.app`)
6. Railway will automatically detect Python and deploy
7. Your app will be live at the Railway URL!

### Configure CORS (Optional)

If you need to restrict CORS to specific domains:

1. Edit `main.py`
2. Update `allow_origins` with your domain(s)
3. Commit and push (Railway auto-deploys)

## ✅ Checklist

- [ ] Server running locally
- [ ] Camera permissions working
- [ ] Quiz completes successfully
- [ ] Code pushed to GitHub
- [ ] Deployed to Railway
- [ ] Production URL tested

## 🆘 Common Issues

**Camera not working?**

- Use HTTPS (required in production)
- Grant browser permissions
- Check camera isn't used by another app

**WebSocket fails?**

- Check CORS settings in `main.py`
- Ensure backend is running
- Verify Railway URL is accessible

**Need more help?**

- See [README.md](README.md) for detailed docs
- See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for deployment guide

---

**Ready to deploy?** Follow the [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) guide for step-by-step instructions!
