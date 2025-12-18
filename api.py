from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()
df = None


@app.on_event("startup")
def load_data():
    global df
    try:
        df = pd.read_excel("shl_individual_assessments.xlsx")

        # Normalize column names (VERY IMPORTANT)
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        df.fillna("", inplace=True)

        print("Loaded columns:", df.columns.tolist())

    except Exception as e:
        print("Error loading Excel:", e)
        df = None


@app.get("/")
def home():
    return {"message": "SHL Assessment Recommendation API is running"}


@app.post("/recommend")
def recommend(payload: dict):
    if df is None:
        raise HTTPException(status_code=500, detail="Assessment data not loaded")

    job_description = payload.get("job_description", "").lower().strip()

    if not job_description:
        return []

    jd_words = job_description.split()

    def is_relevant(text):
        text = str(text).lower()
        return any(word in text for word in jd_words)

    filtered = df[
        df["simple_test_category"].apply(is_relevant) |
        df["assessment_name"].apply(is_relevant)
    ]

    if filtered.empty:
        filtered = df.head(5)
    else:
        filtered = filtered.head(5)

    return filtered[
        ["assessment_name", "assessment_url"]
    ].to_dict(orient="records")
