from fastapi import FastAPI
from app.schemas import AnalyzeRequest
from app.ml import compute_similarity

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Resume Matcher API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    score = compute_similarity(request.resume_text, request.job_description)
    return {
        "match_score": round(score, 4)
    }