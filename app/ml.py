import os
import torch

torch.set_num_threads(1)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def compute_similarity(resume_text: str, job_description: str) -> float:
    model = get_model()
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    similarity_score = util.cos_sim(resume_embedding, job_embedding)
    return float(similarity_score[0][0])


from app.skills_data import SKILL_KEYWORDS

def extract_skills(text: str) -> set:
    text_lower = text.lower()
    found = {skill for skill in SKILL_KEYWORDS if skill in text_lower}
    return found

def get_skill_gap(resume_text: str, job_description: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }