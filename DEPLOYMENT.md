# 🚀 Deployment Guide

This guide will walk you through deploying the Eye Tracking Quiz Application to Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Railway account ([railway.app](https://railway.app))
- Vercel account ([vercel.com](https://vercel.com))
- Git installed locally

## Step 1: Prepare Your Repository

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Verify all files are committed**
   - `main.py`
   - `view.py`
   - `requirements.txt`
   - `Procfile`
   - `railway.json`
   - `frontend/` directory with all files

## Step 2: Deploy Backend to Railway

### Option A: Deploy via GitHub (Recommended)

1. **Log in to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up or log in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository

3. **Configure Service**
   - Railway will auto-detect Python
   - It will use `Procfile` and `railway.json` automatically
   - No additional configuration needed

4. **Get Your Backend URL**
   - Once deployed, Railway will provide a URL like: `your-app.railway.app`
   - Note this URL - you'll need it for the frontend

5. **Set Environment Variables (Optional)**
   - Go to your service → Variables
   - Add any custom environment variables if needed

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login**
   ```bash
   railway login
   ```

3. **Initialize and Deploy**
   ```bash
   railway init
   railway up
   ```

## Step 3: Deploy Frontend to Vercel

### Option A: Deploy via GitHub (Recommended)

1. **Log in to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up or log in with GitHub

2. **Create New Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - **Important**: Set "Root Directory" to `frontend`

3. **Configure Build Settings**
   - Framework Preset: "Other"
   - Build Command: (leave empty - static site)
   - Output Directory: `.` (current directory)
   - Install Command: (leave empty)

4. **Set Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add:
     - Key: `VITE_BACKEND_URL`
     - Value: `wss://your-railway-app.railway.app` (use your Railway URL)

5. **Update config.js**
   - Edit `frontend/config.js`
   - Replace `your-railway-app.railway.app` with your actual Railway URL
   - Commit and push the change

6. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - Note your Vercel URL (e.g., `your-app.vercel.app`)

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend**
   ```bash
   cd frontend
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add VITE_BACKEND_URL
   # Enter: wss://your-railway-app.railway.app
   ```

## Step 4: Configure CORS

1. **Update Backend CORS Settings**
   - Edit `main.py`
   - Find the CORS middleware configuration
   - Update `allow_origins` with your Vercel URL:
   ```python
   allow_origins=[
       "https://your-vercel-app.vercel.app",
       "https://your-vercel-app.vercel.app"  # Add www version if needed
   ]
   ```

2. **Commit and Push**
   ```bash
   git add main.py
   git commit -m "Update CORS for production"
   git push
   ```

3. **Redeploy**
   - Railway will automatically redeploy on push
   - Or manually trigger redeploy from Railway dashboard

## Step 5: Test Your Deployment

1. **Test Backend**
   - Visit: `https://your-railway-app.railway.app/health`
   - Should return: `{"status": "healthy", "service": "eye-tracking-quiz"}`

2. **Test Frontend**
   - Visit your Vercel URL
   - Click "Start Quiz"
   - Grant camera permissions
   - Verify WebSocket connection works

3. **Test End-to-End**
   - Complete a quiz
   - Verify results page loads
   - Check that eye tracking is working

## Step 6: Custom Domain (Optional)

### Vercel Custom Domain

1. Go to Vercel Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update CORS in `main.py` with new domain

### Railway Custom Domain

1. Go to Railway Service Settings → Networking
2. Add custom domain
3. Configure DNS as instructed
4. Update frontend `config.js` with new domain

## Troubleshooting

### Backend Issues

**Problem**: Railway deployment fails
- **Solution**: Check Railway logs, ensure `requirements.txt` is correct
- **Solution**: Verify `Procfile` format is correct

**Problem**: WebSocket connection fails
- **Solution**: Ensure Railway URL uses `wss://` (secure WebSocket)
- **Solution**: Check CORS configuration in `main.py`

### Frontend Issues

**Problem**: Cannot connect to backend
- **Solution**: Verify `config.js` has correct Railway URL
- **Solution**: Check environment variable `VITE_BACKEND_URL` in Vercel
- **Solution**: Ensure backend is running and accessible

**Problem**: Camera not working
- **Solution**: HTTPS is required for camera access in production
- **Solution**: Verify Vercel is serving over HTTPS

### General Issues

**Problem**: CORS errors
- **Solution**: Update `allow_origins` in `main.py` with exact Vercel URL
- **Solution**: Include both `www` and non-`www` versions if applicable

**Problem**: Environment variables not working
- **Solution**: Redeploy after adding environment variables
- **Solution**: Verify variable names match exactly (case-sensitive)

## Post-Deployment Checklist

- [ ] Backend is accessible and healthy
- [ ] Frontend loads correctly
- [ ] WebSocket connection establishes
- [ ] Camera permissions work
- [ ] Eye tracking detects face
- [ ] Quiz questions load and work
- [ ] Results page displays correctly
- [ ] CORS is properly configured
- [ ] All environment variables are set
- [ ] Custom domains configured (if applicable)

## Monitoring

### Railway Monitoring
- View logs in Railway dashboard
- Monitor resource usage
- Set up alerts for errors

### Vercel Monitoring
- View deployment logs
- Monitor analytics
- Check function logs (if using serverless functions)

## Updates and Maintenance

### Updating Backend
1. Make changes to code
2. Commit and push to GitHub
3. Railway auto-deploys on push
4. Monitor deployment logs

### Updating Frontend
1. Make changes to `frontend/` directory
2. Commit and push to GitHub
3. Vercel auto-deploys on push
4. Verify deployment in Vercel dashboard

## Cost Considerations

### Railway
- Free tier: $5 credit/month
- Pay-as-you-go after free tier
- Monitor usage in dashboard

### Vercel
- Free tier: Generous limits for personal projects
- Pro tier: For production/commercial use
- Check current pricing at vercel.com/pricing

---

**Need Help?** Check the main README.md for more detailed information.

