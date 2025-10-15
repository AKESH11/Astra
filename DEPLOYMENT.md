# 🚀 ASTRA Frontend Deployment Guide

## Quick Deploy Options

Your ASTRA frontend is now ready to be deployed! Choose one of these options:

---

## Option 1: GitHub Pages (Recommended - Free)

### Steps:

1. **The `gh-pages` branch is already created** with your frontend files

2. **Push the gh-pages branch:**
```bash
git push origin gh-pages
```

3. **Enable GitHub Pages:**
   - Go to https://github.com/AKESH11/Astra/settings/pages
   - Under "Source", select branch: `gh-pages`
   - Click "Save"

4. **Your site will be live at:**
```
https://akesh11.github.io/Astra/
```

**Note:** For the backend to work, you'll need to deploy it separately (see Backend Deployment below)

---

## Option 2: Netlify (Also Free, Easier)

### Steps:

1. **Go to:** https://app.netlify.com/

2. **Sign up/Login** with GitHub

3. **Click "Add new site" → "Import an existing project"**

4. **Connect your GitHub** repository (AKESH11/Astra)

5. **Configure:**
   - Branch: `gh-pages` (or `main`)
   - Build command: (leave empty)
   - Publish directory: `.` (or `frontend`)

6. **Deploy!**

Your site will be live at: `https://your-site-name.netlify.app`

---

## Option 3: Vercel (Also Free)

### Steps:

1. **Go to:** https://vercel.com/

2. **Sign up/Login** with GitHub

3. **Click "Add New" → "Project"**

4. **Import** your GitHub repository

5. **Configure:**
   - Framework: None
   - Root Directory: `frontend` (or `.` if using gh-pages branch)
   - Build command: (leave empty)

6. **Deploy!**

Your site will be live at: `https://your-project.vercel.app`

---

## 🔧 Backend Deployment (Required for Full Functionality)

Your frontend needs the backend services to work. Here are options:

### Option 1: Local Backend (For Demo)
Keep your backend running locally and demo from your laptop.

### Option 2: Deploy Backend to Cloud

#### A. **Railway.app** (Recommended - Free tier)
1. Go to https://railway.app/
2. Sign up with GitHub
3. Create new project
4. Deploy each service separately or use Docker
5. Update `API_URL` in your frontend with the deployed URL

#### B. **Render.com** (Free tier)
1. Go to https://render.com/
2. Sign up with GitHub
3. Create web services for each microservice
4. Update frontend API_URL

#### C. **Heroku** (Has free tier)
1. Deploy each service as a separate Heroku app
2. Update frontend API_URL

#### D. **DigitalOcean/AWS/Azure** (Paid but professional)
- Use Docker Compose
- Deploy all services together
- Most scalable option

---

## 📝 Important: Update API URL

After deploying your backend, update the `API_URL` in your frontend:

**File:** `index.html` (line ~88)

```javascript
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : 'https://your-actual-backend-url.com'; // <-- Update this!
```

---

## 🎯 For Demo/Competition

### Quick Option (Recommended):
1. **Deploy frontend** to GitHub Pages/Netlify (takes 2 minutes)
2. **Run backend locally** during your demo
3. Share the live frontend link: "Check out our UI at [your-url]"
4. For the actual demo, show it working with your local backend

### Professional Option:
1. **Deploy both** frontend and backend to cloud
2. Share fully working live demo URL
3. More impressive but takes more time to set up

---

## 🔗 Your Deployment URLs

Once deployed, update this section:

- **Frontend (Live UI):** https://akesh11.github.io/Astra/
- **Backend (API):** (run locally or deploy to Railway/Render)
- **GitHub Repo:** https://github.com/AKESH11/Astra

---

## ⚡ Quick Deploy Now (GitHub Pages)

Run these commands:

```bash
# Make sure you're on gh-pages branch
git checkout gh-pages

# Commit any changes
git add .
git commit -m "Deploy frontend to GitHub Pages"

# Push to GitHub
git push origin gh-pages
```

Then enable GitHub Pages in your repository settings!

---

## 🎥 For Your Demo Video

You can use either:
1. **Local version** - `file:///path/to/frontend/index.html` (with services running)
2. **Deployed version** - `https://akesh11.github.io/Astra/` (looks more professional!)

---

## ✅ Checklist

- [ ] Frontend deployed to GitHub Pages/Netlify/Vercel
- [ ] Backend services accessible (local or deployed)
- [ ] API_URL updated in frontend
- [ ] Test that frontend can connect to backend
- [ ] Share live URL in your README
- [ ] Add live demo link to your presentation

---

## 💡 Pro Tip

For the competition, you can:
1. Deploy frontend (looks professional with a real URL)
2. Demo with local backend (easier, no cloud setup needed)
3. Mention "Backend can be deployed to Railway/AWS/Azure for production"

This shows both that it works AND that you understand deployment architecture!

---

Good luck with your deployment! 🚀
