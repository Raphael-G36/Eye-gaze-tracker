# 🚂 Railway Deployment Guide

Complete guide to deploy your Eye Tracking Quiz Application on Railway.

## 📋 Prerequisites

- GitHub account (free)
- Railway account ([railway.app](https://railway.app)) - Free tier available
- Git installed on your computer

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code

1. **Make sure all files are ready:**
   - ✅ `main.py` - Your FastAPI application
   - ✅ `view.py` - Eye tracking logic
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `Procfile` - Railway startup command
   - ✅ `railway.json` - Railway configuration
   - ✅ `templates/` - HTML templates (landing page, quiz, results)
   - ✅ `runtime.txt` - Python version

2. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Ready for Railway deployment"
   ```

### Step 2: Push to GitHub

1. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it (e.g., `eye-tracking-quiz`)
   - Don't initialize with README (you already have files)
   - Click "Create repository"

2. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

### Step 3: Deploy to Railway

#### Option A: Via Railway Website (Recommended - Easiest)

1. **Sign up/Login to Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Sign up with GitHub (recommended) or email

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub (if first time)
   - Select your repository from the list
   - Click "Deploy Now"

3. **Railway Auto-Detection:**
   - Railway will automatically detect it's a Python project
   - It will read `Procfile` and `railway.json`
   - Build will start automatically
   - You'll see build logs in real-time

4. **Wait for Deployment:**
   - First deployment takes 2-5 minutes
   - Watch the build logs for progress
   - You'll see: "Installing dependencies", "Building", "Starting"

5. **Get Your URL:**
   - Once deployed, Railway provides a URL like: `your-app.railway.app`
   - Click on your service → Settings → Generate Domain
   - Copy this URL - this is your live application!

#### Option B: Via Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```
   (Requires Node.js - download from [nodejs.org](https://nodejs.org))

2. **Login:**
   ```bash
   railway login
   ```
   This opens your browser to authenticate.

3. **Initialize Project:**
   ```bash
   railway init
   ```
   Follow the prompts to create a new project.

4. **Deploy:**
   ```bash
   railway up
   ```
   This will build and deploy your application.

### Step 4: Configure Your Deployment

1. **Check Environment Variables:**
   - Go to your Railway project → Variables
   - Railway sets `PORT` automatically (don't change it)
   - Add any custom variables if needed

2. **Check Build Settings:**
   - Railway should auto-detect:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - If not, verify `Procfile` and `railway.json` are correct

3. **Custom Domain (Optional):**
   - Go to Settings → Networking
   - Click "Generate Domain" or add custom domain
   - Update CORS in `main.py` if using custom domain

### Step 5: Test Your Deployment

1. **Visit Your URL:**
   - Open `https://your-app.railway.app` in your browser
   - You should see the landing page

2. **Test the Quiz:**
   - Click "Show Demo" button
   - Grant camera permissions
   - Start the quiz
   - Verify eye tracking works

3. **Check Logs:**
   - In Railway dashboard → Deployments → View Logs
   - Look for any errors or warnings

## 🔧 Troubleshooting

### Build Fails

**Problem:** Build fails during `pip install`

**Solutions:**
- Check `requirements.txt` for typos
- Ensure all dependencies are listed
- Check Railway logs for specific error
- Try removing version pins if a package fails

### Application Won't Start

**Problem:** App deploys but shows error page

**Solutions:**
- Check Railway logs for startup errors
- Verify `Procfile` has correct command
- Ensure `main.py` is in root directory
- Check that `templates/` folder exists

### Camera Not Working

**Problem:** Camera doesn't work in production

**Solutions:**
- Railway servers don't have cameras
- This app requires local camera access
- Railway deployment is for testing/demo
- For production, users need to run locally or use a different setup

**Note:** Railway is a server environment without camera access. The eye tracking will only work when:
- Running locally on your machine
- Users access from their own computers with cameras

### WebSocket Connection Fails

**Problem:** WebSocket can't connect

**Solutions:**
- Ensure Railway URL uses `wss://` (secure WebSocket)
- Check CORS settings in `main.py`
- Verify WebSocket endpoint `/ws` is accessible
- Check Railway logs for connection errors

## 📝 Important Notes

### Camera Limitation

⚠️ **Important:** Railway servers don't have cameras. The eye tracking feature requires:
- Local deployment (your computer)
- Or users accessing from their own devices with cameras

Railway deployment is great for:
- ✅ Testing the application structure
- ✅ Sharing the UI/UX
- ✅ Demo purposes
- ❌ Not for actual eye tracking (needs local camera)

### For Production Use

If you need production eye tracking:
1. **Self-hosted:** Deploy on a server with camera access
2. **Client-side:** Use browser-based camera API (current setup)
3. **Hybrid:** Backend on Railway, frontend serves camera locally

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Deployment successful
- [ ] Application URL accessible
- [ ] Landing page loads
- [ ] Quiz page loads
- [ ] WebSocket connects (check browser console)
- [ ] No errors in Railway logs

## 🔄 Updating Your Deployment

To update your deployed app:

1. **Make changes locally**
2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. **Railway auto-deploys:**
   - Railway detects the push
   - Automatically rebuilds and redeploys
   - Usually takes 2-3 minutes

## 💰 Railway Pricing

- **Free Tier:** $5 credit/month
- **Hobby Plan:** $5/month (if free credit runs out)
- **Pro Plan:** $20/month (for production)

For this app, the free tier should be sufficient for testing and demos.

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

---

**Need Help?** Check the main [README.md](README.md) or Railway logs for detailed error messages.

