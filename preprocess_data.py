# preprocess_dataset.py
import pandas as pd
import ast

# Load raw dataset
df = pd.read_csv("dateset_merged.csv")

cleaned_rows = []

for i, row in df.iterrows():
    try:
        # Parse the JSON-like structure in resume_text
        parsed = ast.literal_eval(row["resume_text"])

        # Extract experiences
        experiences = [exp.get("title", "") for exp in parsed if isinstance(exp, dict) and "title" in exp]
        role = experiences[0] if experiences else "Unknown"

        # Extract skills (if available in technical_environment or projects)
        skills = []
        for exp in parsed:
            if isinstance(exp, dict):
                if "technical_environment" in exp and exp["technical_environment"]:
                    tech = exp["technical_environment"].get("technologies", [])
                    if tech:
                        skills.extend(tech)
                if "responsibilities" in exp and exp["responsibilities"]:
                    skills.extend(exp["responsibilities"])
                if "role" in exp and exp["role"] not in ["unknown", None]:
                    role = exp["role"]

        text = " ".join(experiences + skills)

        cleaned_rows.append({"resume_text": text, "role": role})

    except Exception as e:
        print(f"Skipping row {i} due to error: {e}")

# Convert to DataFrame
cleaned_df = pd.DataFrame(cleaned_rows)

# Ensure no empty rows
cleaned_df = cleaned_df[cleaned_df["resume_text"].str.strip().astype(bool)]

# If role is missing, mark as Unknown
cleaned_df["role"] = cleaned_df["role"].fillna("Unknown")

# Save
cleaned_df.to_csv("cleaned_resumes.csv", index=False)
print(f"✅ Cleaned dataset saved. Rows: {len(cleaned_df)}")
print("Unique roles:", cleaned_df["role"].unique()[:20])  # preview first 20 unique roles
