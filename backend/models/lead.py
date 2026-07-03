from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from datetime import datetime
from backend.database.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=True)  # Added to store lead's industry sector
    source = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)

    # AI-generated analysis fields
    analysis = Column(Text, nullable=True)  # JSON-serialized string of LeadAnalysisResult
    qualification_score = Column(Float, nullable=True)
    is_qualified = Column(Boolean, nullable=True)
    
    # AI-generated scoring & priority fields
    lead_score = Column(Integer, nullable=True)
    priority = Column(String(50), nullable=True)
    confidence = Column(Integer, nullable=True)
    reasoning = Column(Text, nullable=True)  # JSON-serialized list of strings
    
    # Outreach fields
    email_subject = Column(String(255), nullable=True)
    email_body = Column(Text, nullable=True)

    status = Column(String(50), default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
