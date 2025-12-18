from fastapi import FastAPI
import pandas as pd

app = FastAPI()

df = pd.read_excel("shl_individual_assessments.xlsx")

@app.get("/")
def home():
    return {"message": "SHL Assessment Recommendation API is running"}

@app.get("/recommend")
def recommend(job_role: str):
    results = df[
        df["Relevant Job Roles"]
        .str.contains(job_role, case=False, na=False)
    ]
    return results.head(5).to_dict(orient="records")
