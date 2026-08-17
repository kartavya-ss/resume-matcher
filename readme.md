# Resume Matcher

An AI-powered tool that scores how well a resume matches a job description using semantic similarity — not just keyword matching — and highlights specific matched/missing skills.

**Live App:** https://lustrous-bunny-0875d6.netlify.app
**API Docs:** https://resume-matcher-api-fr74.onrender.com/docs

## Why This Project

Most resume-matching tools rely on simple keyword overlap, which fails when a resume says "5 years of ML experience" and a job description says "seasoned machine learning professional" — zero shared words, same meaning. This project uses sentence embeddings to compare meaning, not just vocabulary.

## Architecture

Browser (HTML/CSS/JS) → FastAPI Backend → sentence-transformers (embeddings) → PostgreSQL (persistence)

- Frontend: static HTML/CSS/JS, deployed on Netlify
- Backend: FastAPI (Python), deployed on Render
- ML: `all-MiniLM-L6-v2` sentence embeddings + cosine similarity
- Database: PostgreSQL via SQLAlchemy ORM

## Key Design Decisions

| Decision | Why |
|---|---|
| Embeddings over keyword matching | Captures semantic meaning, handles synonyms/phrasing differences |
| FastAPI over Flask/Django | Auto validation + auto-generated docs, lighter than Django for this scope |
| PostgreSQL over MongoDB | Data is structured and predictable — a relational fit |
| CPU-only PyTorch build | Free-tier hosting has a 512MB memory cap; GPU-enabled torch caused OOM crashes |
| Lazy model loading | Loading the ML model at import time delayed server startup past Render's timeout; loading on first request fixed it |

## Features

- Paste resume text OR upload a PDF resume
- Semantic match scoring (not just keyword overlap)
- Matched vs. missing skill breakdown
- Analysis history, persisted to PostgreSQL
- Full error handling (invalid PDFs, empty fields, malformed requests)
- Automated unit tests (pytest) for core ML logic

## Tech Stack

Python, FastAPI, SQLAlchemy, PostgreSQL, sentence-transformers, pytest, HTML/CSS/JavaScript, Git, deployed on Render + Netlify

## Running Locally

\`\`\`bash
git clone https://github.com/kartavya-ss/resume-matcher.git
cd resume-matcher
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# create a .env file with DATABASE_URL=your_postgres_url
python create_tables.py
uvicorn app.main:app --reload
\`\`\`

Then open \`frontend/index.html\` via a local server (e.g. \`python -m http.server 5500\`).

## A Real Debugging Story

Deployment initially failed with an out-of-memory crash. I diagnosed it as PyTorch's default GPU-enabled build consuming too much of Render's 512MB free-tier limit, switched to the CPU-only build, then hit a second issue — the embedding model loading at import time delayed server startup past Render's boot timeout. Fixed by lazy-loading the model on first request instead of at startup.

## Future Improvements

- Normalize matched/missing skills into a separate DB table for efficient querying
- Add OCR support for scanned/image-based PDFs
- Move skill extraction from keyword-matching to a fine-tuned NER model