import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load expanded dataset
df = pd.read_csv("expanded_jobs.csv")

# Features & labels
X = df["description"]
y = df["role"]

# Vectorizer + Model
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=300, class_weight="balanced")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with accuracy: {acc:.2f}")

# Save
joblib.dump(model, "career_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
