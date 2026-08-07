from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    candidate_name: str
    resume_text: str
    job_description: str