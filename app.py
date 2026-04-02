from flask import Flask, render_template, request
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load pipeline model (vectorizer + classifier together)
model = joblib.load("model.pkl")

# Example job metadata (extend this as needed)
job_metadata = {
    "Software Engineer": {
        "salary_low": 6, "salary_high": 18,
        "growth": "High",
        "cities": ["Bangalore", "Hyderabad", "Pune"],
        "desc": "Develops, tests, and maintains software applications."
    },
    "Financial Analyst": {
        "salary_low": 5, "salary_high": 15,
        "growth": "Medium",
        "cities": ["Mumbai", "Delhi", "Chennai"],
        "desc": "Analyzes financial data to guide investment and business decisions."
    },
    "AI Researcher": {
        "salary_low": 10, "salary_high": 25,
        "growth": "Very High",
        "cities": ["Bangalore", "Hyderabad"],
        "desc": "Works on advanced AI models, deep learning, and data-driven innovation."
    },
    "Sales Manager": {
        "salary_low": 4, "salary_high": 12,
        "growth": "Medium",
        "cities": ["Delhi", "Mumbai", "Bangalore"],
        "desc": "Leads a sales team to achieve revenue goals and client acquisition."
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    file = request.files["resume"]
    text = file.read().decode("utf-8", errors="ignore")

    # Use pipeline directly
    probs = model.predict_proba([text])[0]
    roles = model.classes_

    # Get top 3 predictions
    top_indices = np.argsort(probs)[::-1][:3]
    results = []
    for idx in top_indices:
        role = roles[idx]
        prob = probs[idx]
        meta = job_metadata.get(role, {})
        results.append({
            "role": role,
            "prob": float(prob),
            "salary_low": meta.get("salary_low", 4),
            "salary_high": meta.get("salary_high", 10),
            "growth": meta.get("growth", "Unknown"),
            "cities": meta.get("cities", []),
            "desc": meta.get("desc", "No description available.")
        })

    return render_template("results.html", results=results, accuracy=0.86)

if __name__ == "__main__":
    app.run(debug=True)
