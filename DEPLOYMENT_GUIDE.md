# Nexus AI - Deployment Guide

## 🌐 Netlify Deployment (Frontend Only)

Your frontend is now deployed on Netlify, but **the backend cannot run on Netlify** because:
- Netlify only hosts static files (HTML/CSS/JS)
- Your Python backend needs a server environment
- Ollama/Mistral needs to run locally

## ✅ Two Options:

### Option 1: Local Backend + Netlify Frontend (Recommended for Development)
1. Run backend locally: `python backend/app.py`
2. Frontend works on Netlify but connects to your local backend
3. **Note:** This only works when your computer is running the backend

### Option 2: Deploy Backend Separately (Recommended for Production)

Deploy your backend to a hosting service that supports Python:

#### **A) Railway.app (Easiest)**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### **B) Render.com (Free Tier)**
1. Go to https://render.com
2. Connect your GitHub repo
3. Create new "Web Service"
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python backend/app.py`

#### **C) Heroku**
```bash
heroku create nexus-ai-backend
git push heroku main
```

#### **D) DigitalOcean App Platform**
1. Connect GitHub repo
2. Auto-detect Python
3. Deploy

### Option 3: Full Local Setup (No Cloud)
Run everything locally:
```bash
.\run_server.bat
```
Access at: http://localhost:8000

## 🔧 Current Setup

- **Frontend (Netlify):** ✅ Works (static files)
- **Backend:** ❌ Needs separate hosting
- **Firebase Auth:** ✅ Works on Netlify

## 📝 Next Steps

1. **Keep Netlify for frontend** (it's already working)
2. **Deploy backend to Railway/Render**
3. **Update frontend to use backend URL**

Need help? Let me know which option you prefer!
