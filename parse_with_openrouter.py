import os
import json
import requests

# -------- PDF/TXT extraction (no extra heavy deps) --------
def extract_resume_text(file_path: str) -> str:
    """
    Minimal PDF/TXT reader:
      - If .txt: read as text (utf-8)
      - If .pdf: try PyPDF2 if installed; else return empty string
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""
    elif ext == ".pdf":
        try:
            from PyPDF2 import PdfReader  # pure python, small install
            text_parts = []
            reader = PdfReader(file_path)
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
            return "\n".join(text_parts)
        except Exception:
            # PyPDF2 is not installed or failed to read — suggest saving resume as .txt next time
            return ""
    else:
        return ""


# -------- OpenRouter enrichment (optional) --------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini").strip()

def _chat_openrouter(system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 300):
    """
    Call OpenRouter chat completions. Returns content string or None on failure.
    If no API key, returns None.
    """
    if not OPENROUTER_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return content
    except Exception:
        return None


def gpt_enrich_role_info(role: str):
    """
    Optionally enrich job description, salary band, and best cities via OpenRouter.
    Returns dict or None. Safe to call; returns None if key/rate-limit error.
    """
    system = "You are a concise career assistant for the Indian job market."
    user = f"""
Given the role: "{role}", return a compact JSON with keys:
- job_description: 1-2 sentences (max 45 words)
- salary_lpa: object with low and high (numbers in INR LPA)
- cities_india: array of up to 5 Indian cities with strong growth for this role

Only return JSON. Example:
{{
  "job_description": "…",
  "salary_lpa": {{"low": 6, "high": 18}},
  "cities_india": ["Bengaluru","Hyderabad","Pune"]
}}
"""
    content = _chat_openrouter(system, user, temperature=0.3, max_tokens=200)
    if not content:
        return None

    # Try to parse JSON inside code fences or raw
    txt = content.strip()
    if txt.startswith("```"):
        # remove ```json ... ```
        txt = txt.strip("`")
        # After stripping backticks, the first line might be 'json'
        lines = txt.splitlines()
        if lines and lines[0].lower().strip() == "json":
            txt = "\n".join(lines[1:])

    try:
        return json.loads(txt)
    except Exception:
        # Try extracting the first {...} block
        start = txt.find("{")
        end = txt.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(txt[start : end + 1])
            except Exception:
                return None
        return None
