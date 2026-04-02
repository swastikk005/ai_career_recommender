from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import pandas as pd
import json
import os
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from the root directory
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
load_dotenv() # Also check local backend/.env as fallback

# Check for API Key
if not os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    print("\n[WARNING] No API Key (OpenAI or OpenRouter) found in project root .env")
    print("AI features like Detailed Roadmaps and Chat will use fallback logic.\n")

app = FastAPI(title="AI Career Recommendation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load existing ML model
MODEL_PATH = "../model.pkl" # Adjusted path since we are in backend/
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Existing ML model loaded successfully.")
    else:
        # Fallback if model doesn't exist yet in the right place
        model = None
        print(f"Warning: model.pkl not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load career metadata
CAREERS_DATA_PATH = "data/careers.json"
try:
    with open(CAREERS_DATA_PATH, "r") as f:
        careers_metadata = json.load(f)
except Exception as e:
    print(f"Error loading careers data: {e}")
    careers_metadata = []

class UserInput(BaseModel):
    name: str
    degree: str
    skills: str
    interests: str
    experience: str
    industry: str

@app.get("/")
async def root():
    return {"message": "AI Career Recommendation API is running"}

from app.services.resume_parser import ResumeParser
from app.services.ai_service import AIService

@app.post("/recommend")
async def recommend_careers(
    resume: UploadFile = File(...)
):
    resume_text = ""
    parsed_resume = {}
    
    file_bytes = await resume.read()
    resume_text = ResumeParser.extract_text(file_bytes, resume.filename)
    
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from resume")

    # Use AI to parse resume
    parsed_resume = AIService.parse_resume(resume_text)
    
    if not parsed_resume:
         # Basic fallback if parsing fails but we have text
         parsed_resume = {"skills": [], "degree": "", "experience": ""}

    name = parsed_resume.get('name', 'User')
    skills = ', '.join(parsed_resume.get('skills', []))
    degree = parsed_resume.get('degree', '')
    experience = str(parsed_resume.get('experience', ''))
    interests = "General" 
    industry = "Technology" 

    input_text = f"{skills} {experience} {degree}"
    
    user_profile = {
        "name": name,
        "degree": degree,
        "skills": skills,
        "interests": interests,
        "experience": experience,
        "industry": industry,
        "resume_text": resume_text[:1000]
    }

    results = []
    
    # Attempt OpenAI recommendations first for feature-rich output
    recommendations = AIService.get_career_recommendations(user_profile)
    
    if recommendations:
        # If OpenAI works, use its detailed output
        # Ensure it follows the expected format or convert it
        if isinstance(recommendations, list):
            results = recommendations
        elif isinstance(recommendations, dict) and "recommendations" in recommendations:
            results = recommendations["recommendations"]
        else:
            results = recommendations
    if not results:
        # Ultimate fallback if no model and no AI response
        role = "Software Engineer"
        meta = next((c for c in careers_metadata if c["career"] == role), None)
        results = [{
            "career": role,
            "confidence": 50,
            "salary": meta["salary"] if meta else "₹8-20 LPA",
            "demand": meta["demand"] if meta else "High",
            "growth": meta["growth"] if meta else "25%",
            "skills_required": meta["skills"] if meta else ["Java", "System Design", "Algorithms"],
            "description": meta["description"] if meta else "Development and maintenance of software systems.",
            "skill_gap": ["Cloud Computing"],
            "roadmap": "### Learning Roadmap\n1. Master Data Structures\n2. Learn Cloud Fundamentals\n3. Build Portfolio Projects"
        }]

    # Get resume score if resume is present
    resume_analysis = {}
    if resume_text:
        resume_analysis = AIService.get_resume_score(resume_text)
        if not resume_analysis:
            resume_analysis = {"score": 70, "improvement_suggestions": ["Add more metrics", "Quantify results"]}

    return {
        "user": name,
        "parsed_info": parsed_resume,
        "resume_analysis": resume_analysis,
        "recommendations": results
    }

@app.post("/chat")
async def career_advisor_chat(message: str = Form(...), profile: str = Form(...)):
    # Simple endpoint for AI Chat Advisor
    try:
        user_profile = json.loads(profile)
        response = AIService.chat_advisor(message, user_profile)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
