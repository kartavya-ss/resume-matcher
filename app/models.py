from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    match_score = Column(Float, nullable=False)
    matched_skills = Column(String, default="")
    missing_skills = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())