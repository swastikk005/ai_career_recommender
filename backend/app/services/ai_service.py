import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the root directory
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv() # Also check local backend/.env as fallback

# Initialize the OpenAI client lazily to avoid crashing if key is missing
def get_openai_client():
    # Support both OpenRouter and OpenAI key names
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        # Check if it's an OpenRouter key (usually starts with sk-or-)
        is_openrouter = api_key.startswith("sk-or-")
        
        if is_openrouter:
            return OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "http://localhost:3000", # Required for OpenRouter
                    "X-Title": "AI Career Recommender",      # Optional for OpenRouter
                }
            )
        else:
            return OpenAI(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}")
        return None

class AIService:
    @staticmethod
    def _get_json_response(prompt: str, system_prompt: str = "You are a career expert.", model: str = "gpt-3.5-turbo"):
        """Helper to get a clean JSON response from OpenAI."""
        client = get_openai_client()
        if not client:
            return None
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt + " ALWAYS return valid JSON. No preamble."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"} if model == "gpt-4-1106-preview" or model == "gpt-3.5-turbo-1106" or model == "gpt-4o" else None
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI error in {model}: {e}")
            return None

    @staticmethod
    def parse_resume(resume_text: str):
        """Extract skills, experience, and education from resume text."""
        prompt = f"""
        Analyze the following resume text and extract key information in JSON format:
        {{
          "name": "Full Name",
          "degree": "Highest Degree",
          "skills": ["Skill 1", "Skill 2"],
          "experience": "Total Years (e.g., 2)",
          "technologies": ["Tech 1", "Tech 2"],
          "education": "University Name",
          "projects": ["Project 1"]
        }}

        Resume Text:
        {resume_text}
        """
        return AIService._get_json_response(prompt, "You are an expert HR parser.")

    @staticmethod
    def get_career_recommendations(user_profile: dict):
        """Get 5 career recommendations based on user profile."""
        prompt = f"""
        Based on the following user profile, recommend the top 5 careers.
        Return a JSON object with a 'recommendations' key containing a list of:
        {{
          "career": "Career Name",
          "confidence": "percentage (0-100)",
          "skills_required": ["Required Skill 1", "Required Skill 2"],
          "salary": "Salary Range (e.g., ₹8-20 LPA)",
          "demand": "High/Medium/Low",
          "growth": "Growth Percentage (e.g., 25%)",
          "description": "Short overview of the role",
          "skill_gap": ["What's missing from user's current skills"],
          "roadmap": "A markdown formatted step-by-step learning path"
        }}

        User Profile:
        {json.dumps(user_profile)}
        """
        # For OpenRouter, use 'openai/gpt-3.5-turbo' or 'google/gemini-pro-1.5' etc.
        # But standard 'gpt-3.5-turbo' also works on OpenRouter usually.
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")
        is_openrouter = api_key.startswith("sk-or-")
        model = "openai/gpt-3.5-turbo" if is_openrouter else "gpt-3.5-turbo"
        
        return AIService._get_json_response(prompt, "You are a senior career advisor.", model=model)

    @staticmethod
    def get_resume_score(resume_text: str):
        """Calculate a resume score and provide improvement suggestions."""
        prompt = f"""
        Rate the following resume (1-100) and provide improvement suggestions in JSON:
        {{
          "score": 85,
          "breakdown": {{ "impact": 80, "skills": 90, "formatting": 85, "relevance": 82 }},
          "improvement_suggestions": ["Suggestion 1", "Suggestion 2", "Suggestion 3"]
        }}

        Resume Text:
        {resume_text[:2000]}
        """
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")
        is_openrouter = api_key.startswith("sk-or-")
        model = "openai/gpt-3.5-turbo" if is_openrouter else "gpt-3.5-turbo"
        return AIService._get_json_response(prompt, "You are a professional resume reviewer.", model=model)

    @staticmethod
    def chat_advisor(message: str, profile: dict):
        """Career chat advisor response."""
        client = get_openai_client()
        if not client:
            return "OpenAI API Key is missing. Please add it to your .env file to enable the Chat Advisor."
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")
        is_openrouter = api_key.startswith("sk-or-")
        model = "openai/gpt-3.5-turbo" if is_openrouter else "gpt-3.5-turbo"
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a helpful AI Career Advisor. User Context: {profile}"},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"
