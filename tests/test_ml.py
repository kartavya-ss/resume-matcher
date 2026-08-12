import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ml import compute_similarity, extract_skills, get_skill_gap

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ml import compute_similarity, extract_skills, get_skill_gap


def test_compute_similarity_identical_text():
    score = compute_similarity("Python developer", "Python developer")
    assert score > 0.99


def test_compute_similarity_unrelated_text():
    score = compute_similarity(
        "Experienced Python backend developer with FastAPI skills.",
        "Delicious homemade pasta recipe with tomato sauce."
    )
    assert score < 0.5


def test_extract_skills_finds_known_skill():
    skills = extract_skills("I am skilled in Python and SQL.")
    assert "python" in skills
    assert "sql" in skills


def test_extract_skills_ignores_unknown_words():
    skills = extract_skills("I like painting and hiking.")
    assert "python" not in skills
    assert len(skills) == 0


def test_get_skill_gap_matched_and_missing():
    result = get_skill_gap(
        resume_text="Skilled in Python and Docker.",
        job_description="Looking for Python, Docker, and AWS experience."
    )
    assert "python" in result["matched_skills"]
    assert "docker" in result["matched_skills"]
    assert "aws" in result["missing_skills"]