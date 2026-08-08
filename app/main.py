from fastapi import FastAPI, UploadFile, File, Form
from app.schemas import AnalyzeRequest
from app.ml import compute_similarity, get_skill_gap
from app.pdf_utils import extract_text_from_pdf

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
    skill_gap = get_skill_gap(request.resume_text, request.job_description)
    return {
        "match_score": round(score, 4),
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"]
    }

@app.post("/analyze-pdf")
async def analyze_pdf(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    file_bytes = await resume_file.read()
    resume_text = extract_text_from_pdf(file_bytes)

    score = compute_similarity(resume_text, job_description)
    skill_gap = get_skill_gap(resume_text, job_description)

    return {
        "match_score": round(score, 4),
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "extracted_text_preview": resume_text[:200]
    }