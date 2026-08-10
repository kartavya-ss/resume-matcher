from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.schemas import AnalyzeRequest
from app.ml import compute_similarity, get_skill_gap
from app.pdf_utils import extract_text_from_pdf
from app.database import SessionLocal
from app.models import Analysis

app = FastAPI()

# --- DATABASE SETUP ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- HEALTH ROUTES ---
@app.get("/")
def read_root():
    return {"message": "Resume Matcher API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- 1. TEXT ANALYZE ROUTE (Saves to DB) ---
@app.post("/analyze")
def analyze(request: AnalyzeRequest, db: Session = Depends(get_db)):
    score = compute_similarity(request.resume_text, request.job_description)
    skill_gap = get_skill_gap(request.resume_text, request.job_description)

    # Save to PostgreSQL
    record = Analysis(
        match_score=round(score, 4),
        matched_skills=",".join(skill_gap["matched_skills"]),
        missing_skills=",".join(skill_gap["missing_skills"])
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "match_score": record.match_score,
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"]
    }

# --- 2. PDF ANALYZE ROUTE (Homework: Now saves to DB too!) ---
@app.post("/analyze-pdf")
async def analyze_pdf(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db) # <-- Added the database dependency
):
    file_bytes = await resume_file.read()
    resume_text = extract_text_from_pdf(file_bytes)
    
    score = compute_similarity(resume_text, job_description)
    skill_gap = get_skill_gap(resume_text, job_description)
    
    # <-- ADDED DATABASE SAVING LOGIC HERE -->
    record = Analysis(
        match_score=round(score, 4),
        matched_skills=",".join(skill_gap["matched_skills"]),
        missing_skills=",".join(skill_gap["missing_skills"])
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {
        "id": record.id, # Returns the new database ID
        "match_score": round(score, 4),
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "extracted_text_preview": resume_text[:200]
    }

# --- 3. HISTORY ROUTE (Fetches from DB) ---
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(Analysis).order_by(Analysis.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "match_score": r.match_score,
            "matched_skills": r.matched_skills.split(",") if r.matched_skills else [],
            "missing_skills": r.missing_skills.split(",") if r.missing_skills else [],
            "created_at": r.created_at
        }
        for r in records
    ]