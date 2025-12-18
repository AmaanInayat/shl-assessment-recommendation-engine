from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Load data once
df = pd.read_excel("shl_individual_assessments.xlsx")

@app.get("/")
def home():
    return {"message": "SHL Assessment Recommendation API is running"}

@app.post("/recommend")
def recommend(payload: dict):
    job_description = payload.get("job_description", "").lower()

    if not job_description:
        return []

    jd_words = job_description.split()

    def is_relevant(text):
        text = str(text).lower()
        return any(word in text for word in jd_words)

    filtered = df[
        df["Simple_Test_Category"].apply(is_relevant) |
        df["Assessment_Name"].apply(is_relevant)
    ]

    if filtered.empty:
        filtered = df.head(5)
    else:
        filtered = filtered.head(5)

    return filtered[
        ["Assessment_Name", "Assessment_URL"]
    ].to_dict(orient="records")
