from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str