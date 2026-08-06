from fastapi import FastAPI
from app.schemas import AnalyzeRequest

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Resume Matcher API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    return {
        "received_resume_length": len(request.resume_text),
        "received_job_description_length": len(request.job_description)
    }