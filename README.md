# AI-Powered Career Recommendation System

An advanced, production-ready career guidance platform built for Final Year Engineering Projects. It combines traditional Machine Learning with modern Generative AI to provide precision career matching, skill gap analysis, and personalized learning roadmaps.

## 🚀 Features

-   **Resume Parsing**: Automatically extracts skills, experience, and education from PDF/DOCX using OpenAI.
-   **Hybrid Recommendation Engine**: Uses a pre-trained Random Forest model for initial classification and GPT-4 for deep career matching.
-   **Skill Gap Analysis**: Identifies missing technical and soft skills for target roles.
-   **Learning Roadmap**: Generates step-by-step actionable paths to transition into new careers.
-   **AI Career Advisor**: A real-time chat assistant to answer career-specific questions.
-   **Resume Scoring**: Analyzes resume impact, formatting, and relevance with improvement tips.
-   **Premium UI**: Built with Next.js 14, Tailwind CSS v4, and Framer Motion for a stunning user experience.

## 🛠 Tech Stack

-   **Frontend**: Next.js (App Router), TypeScript, Tailwind CSS v4, Framer Motion, Lucide React.
-   **Backend**: FastAPI (Python), OpenAI API, Scikit-learn, Pandas, Joblib.
-   **AI/ML**: GPT-4 (Recommendations), GPT-3.5 (Parsing/Chat), Random Forest (Base Prediction).

## 📋 Prerequisites

-   Python 3.9+
-   Node.js 18+
-   OpenAI API Key

## 🛠 Setup Instructions

### 1. Backend Setup
1. **Open a new terminal** and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file (copy from `.env.example`) and add your `OPENAI_API_KEY`.
5. Start the server:
   ```bash
   python main.py
   ```

### 2. Frontend Setup
1. **Open a SECOND terminal** and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 🎯 Usage

1. Open `http://localhost:3000` in your browser.
2. Go to the **Get Started** page.
3. Fill in your details and upload your resume.
4. View your personalized **Career Dashboard**.
5. Interact with the **AI Career Advisor** for further guidance.

## 📄 License
MIT License - Created for Educational Purposes.
