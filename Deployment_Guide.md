# 🚀 Deployment Guide: AI Career Recommendation System

This guide outlines the steps to deploy the application to a production environment (e.g., Vercel, Render, AWS).

## 1. Backend Deployment (FastAPI)

### Option A: Render (Easiest)
1. Create a new "Web Service" on [Render](https://render.com).
2. Connect your GitHub repository.
3. Set the **Build Command**: `pip install -r backend/requirements.txt`
4. Set the **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. (Alternative) If you set the **Root Directory** to `backend` on Render:
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add **Environment Variables**:
   - `PYTHON_VERSION`: `3.10.0` (Critical to avoid build issues)
   - `OPENAI_API_KEY`: Your secret key.
   - `MONGODB_URI`: Your database connection string.

### Option B: AWS EC2 / DigitalOcean
1. Provision a Linux server.
2. Clone the repository: `git clone <repo-url>`.
3. Install Python and dependencies.
4. Set up a reverse proxy using **Nginx**.
5. Use **Gunicorn** or **PM2** to keep the process running.

---

## 2. Frontend Deployment (Next.js)

### Option A: Vercel (Recommended)
1. Import your project from GitHub into [Vercel](https://vercel.com).
2. Select the `frontend` directory as the **Root Directory**.
3. Set the **Build Command**: `npm install && npm run build`
4. Set the **Start Command**: `npm start`
5. The build settings should automatically detect Next.js.
6. Add **Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend (e.g., `https://api-career-recommender.onrender.com`).
7. Click **Deploy**.

---

## 3. Database Setup (MongoDB)
1. Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a new cluster and standard database.
3. Whitelist the IP addresses of your deployment servers.
4. Get the connection string and add it to your backend's environment variables.

---

## 5. Troubleshooting Common Issues
- **Error: Could not read package.json**: This happens if Render thinks your project is a Node.js app. 
  - **Solution**: Go to **Settings** on Render and ensure the **Runtime** is set to **Python 3**. Avoid having a `package.json` or `package-lock.json` in the root if you are only deploying the API.
  - **Start Command**: Make sure it is exactly `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.

---

## 💡 Pro Tips for Final Submission
-   **Screenshots**: Add high-quality screenshots to your `README.md`.
-   **Demo Video**: Record a 2-minute walkthrough using tools like Loom.
-   **Live Link**: Provide a live URL for your examiners to test.
