# merge_datasets.py
from datasets import load_dataset
import pandas as pd
import re

def safe_text_join(df, cols):
    existing = [c for c in cols if c in df.columns]
    if not existing:
        return ""
    return df[existing].fillna("").astype(str).agg(" ".join, axis=1)

all_frames = []

# ​​ Attempt to load datasetmaster/resumes
try:
    print("Loading 'datasetmaster/resumes'...")
    ds = load_dataset("datasetmaster/resumes", split="train")
    df = pd.json_normalize(ds)
    df['resume_text'] = safe_text_join(df, [
        "experience", "education", "skills", "projects", "summary", "certifications"
    ])
    df = df[['resume_text']].copy()
    all_frames.append(df)
    print(" → Resumes dataset loaded, records:", len(df))
except Exception as e:
    print("  ! Could not load 'datasetmaster/resumes':", e)

# ​​ Attempt to load JobHop
try:
    print("Loading 'aida-ugent/JobHop'...")
    ds2 = load_dataset("aida-ugent/JobHop", split="train")
    df2 = pd.DataFrame(ds2)
    df2['resume_text'] = safe_text_join(df2, [
        "description", "experience", "education", "skills", "projects", "summary"
    ])
    df2 = df2[['resume_text']].copy()
    all_frames.append(df2)
    print(" → JobHop dataset loaded, records:", len(df2))
except Exception as e:
    print("  ! Could not load 'aida-ugent/JobHop':", e)

# ​​ Attempt to load opensporks/resumes
try:
    print("Loading 'opensporks/resumes'...")
    ds3 = load_dataset("opensporks/resumes", split="train")
    df3 = pd.DataFrame(ds3)
    df3['resume_text'] = safe_text_join(df3, ["Resume_str", "resume_html"])
    df3 = df3[['resume_text']].copy()
    all_frames.append(df3)
    print(" → OpenSpork resumes loaded, records:", len(df3))
except Exception as e:
    print("  ! Could not load 'opensporks/resumes':", e)

if not all_frames:
    raise RuntimeError("No datasets loaded, cannot proceed.")

# Merge and dedupe
merged = pd.concat(all_frames, ignore_index=True)
merged['resume_text'] = merged['resume_text'].str.strip().str.lower()
merged = merged[merged['resume_text'] != ""]
merged.drop_duplicates(subset=["resume_text"], inplace=True)

print("Total merged resumes:", len(merged))

# Save to CSV
merged.to_csv("dataset_merged.csv", index=False)
print("Saved combined dataset to dataset_merged.csv")
