# 🚀 Deployment Guide: AI Career Recommendation System

This guide outlines the steps to deploy the application to a production environment (e.g., Vercel, Render, AWS).

## 1. Backend Deployment (FastAPI)

### Option A: Render (Easiest)
1. Create a new "Web Service" on [Render](https://render.com).
2. Connect your GitHub repository.
3. Set the **Build Command**: `pip install -r backend/requirements.txt`
4. Set the **Start Command**: `python backend/main.py`
5. Add **Environment Variables**:
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
2. Select the `frontend` directory as the root.
3. The build settings should automatically detect Next.js.
4. Add **Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend (e.g., `https://api-career-recommender.onrender.com`).
5. Click **Deploy**.

---

## 3. Database Setup (MongoDB)
1. Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a new cluster and standard database.
3. Whitelist the IP addresses of your deployment servers.
4. Get the connection string and add it to your backend's environment variables.

---

## 4. Final Verification
1. Ensure the frontend `NEXT_PUBLIC_API_URL` correctly points to the deployed backend.
2. Check that the `.env` variables are correctly set in the production environment.
3. Verify that the AI features (parsing, recommendations) work in production.

---

## 💡 Pro Tips for Final Submission
-   **Screenshots**: Add high-quality screenshots to your `README.md`.
-   **Demo Video**: Record a 2-minute walkthrough using tools like Loom.
-   **Live Link**: Provide a live URL for your examiners to test.
