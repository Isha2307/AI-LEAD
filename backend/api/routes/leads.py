from backend.agents import lead_analyzer_agent, lead_scoring_agent, email_generator_agent

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from datetime import datetime
from typing import List, Optional

from backend.database.database import get_db
from backend.models.lead import Lead
from backend.schemas.lead_schema import (
    LeadAnalysisRequest,
    LeadAnalysisOutput,
    LeadAnalysisResult,
    LeadScoringRequest,
    LeadScoringOutput,
    LeadScoringResult,
    EmailGenerationRequest,
    EmailGenerationOutput,
    EmailGenerationResult,
)
from backend.utils.logger import app_logger

router = APIRouter(tags=["leads"])

# Helper function to update/save database lead record
def save_or_update_lead(db: Session, email: str, update_data: dict) -> Lead:
    lead = db.query(Lead).filter(Lead.email == email).first()
    if lead:
        for key, value in update_data.items():
            setattr(lead, key, value)
    else:
        lead = Lead(email=email, **update_data)
        db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.post("/analyze", response_model=LeadAnalysisOutput)
async def analyze_lead_endpoint(request: LeadAnalysisRequest, db: Session = Depends(get_db)):
    app_logger.info(f"POST /leads/analyze - Company: {request.company}")
    try:
        # Run agent analysis
        analysis_result = lead_analyzer_agent.analyze_lead(
            name=request.name,
            email=request.email,
            company=request.company,
            industry=request.industry,
            employee_count=request.employee_count,
            lead_message=request.lead_message
        )
        
        # Calculate qualification score
        score, is_qualified = lead_analyzer_agent.get_qualification_score(analysis_result)
        
        # Database persistence
        db_data = {
            "name": request.name,
            "company": request.company,
            "industry": request.industry,
            "lead_score": int(score),
            "qualification_score": score,
            "is_qualified": is_qualified,
            "analysis": json.dumps(analysis_result.model_dump()),
            "status": "qualified" if is_qualified else "disqualified"
        }
        save_or_update_lead(db, request.email, db_data)
        
        return LeadAnalysisOutput(
            name=request.name,
            email=request.email,
            company=request.company,
            analysis=analysis_result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except ValueError as e:
        app_logger.error(f"Validation error in analyze endpoint: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except RuntimeError as e:
        app_logger.error(f"Gemini API error in analyze endpoint: {e}")
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable. Please try again.")
    except Exception as e:
        app_logger.error(f"Unexpected error in analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post("/score", response_model=LeadScoringOutput)
async def score_lead_endpoint(request: LeadScoringRequest, db: Session = Depends(get_db)):
    app_logger.info(f"POST /leads/score - Company: {request.company}")
    try:
        # Run agent scoring
        scoring_result = lead_scoring_agent.score_lead(
            name=request.name,
            email=request.email,
            company=request.company,
            industry=request.industry,
            employee_count=request.employee_count,
            lead_message=request.lead_message,
            analysis=request.analysis
        )
        
        # Database persistence
        db_data = {
            "name": request.name,
            "company": request.company,
            "industry": request.industry,
            "lead_score": scoring_result.lead_score,
            "priority": scoring_result.priority,
            "confidence": scoring_result.confidence,
            "reasoning": json.dumps(scoring_result.reasoning),
            "is_qualified": scoring_result.lead_score >= 60,
            "status": "qualified" if scoring_result.lead_score >= 60 else "disqualified"
        }
        save_or_update_lead(db, request.email, db_data)
        
        return LeadScoringOutput(
            name=request.name,
            email=request.email,
            company=request.company,
            analysis=request.analysis,
            scoring=scoring_result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except ValueError as e:
        app_logger.error(f"Validation error in score endpoint: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except RuntimeError as e:
        app_logger.error(f"Gemini API error in score endpoint: {e}")
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable. Please try again.")
    except Exception as e:
        app_logger.error(f"Unexpected error in score endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post("/generate-email", response_model=EmailGenerationOutput)
async def generate_email_endpoint(request: EmailGenerationRequest, db: Session = Depends(get_db)):
    app_logger.info(f"POST /leads/generate-email - Company: {request.company}")
    try:
        # Run email generator agent
        email_result = email_generator_agent.generate_email(
            company=request.company,
            requirement=request.requirement,
            budget=request.budget,
            timeline=request.timeline,
            priority=request.priority
        )
        
        # Try to find a lead with this company to save outreach email
        lead = db.query(Lead).filter(Lead.company == request.company).first()
        if lead:
            lead.email_subject = email_result.subject
            lead.email_body = email_result.email
            db.commit()
            
        return EmailGenerationOutput(
            company=request.company,
            requirement=request.requirement,
            priority=request.priority,
            email_content=email_result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except ValueError as e:
        app_logger.error(f"Validation error in generate-email endpoint: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except RuntimeError as e:
        app_logger.error(f"Gemini API error in generate-email endpoint: {e}")
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable. Please try again.")
    except Exception as e:
        app_logger.error(f"Unexpected error in generate-email endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Standard CRUD Routes

@router.post("", response_model=dict)
async def create_lead(lead_data: dict, db: Session = Depends(get_db)):
    email = lead_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    save_or_update_lead(db, email, lead_data)
    return {"message": "Lead created successfully"}

@router.get("/qualified/list", response_model=List[dict])
async def list_qualified_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    leads = db.query(Lead).filter(Lead.is_qualified == True).offset(skip).limit(limit).all()
    return [{
        "id": l.id,
        "name": l.name,
        "email": l.email,
        "company": l.company,
        "qualification_score": l.qualification_score
    } for l in leads]

@router.get("/{lead_id}", response_model=dict)
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    # Return serializable model dictionary
    return {
        "id": lead.id,
        "name": lead.name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "source": lead.source,
        "notes": lead.notes,
        "status": lead.status,
        "qualification_score": lead.qualification_score,
        "is_qualified": lead.is_qualified
    }

@router.get("", response_model=List[dict])
async def list_leads(skip: int = 0, limit: int = 10, status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    leads = query.offset(skip).limit(limit).all()
    return [{
        "id": l.id,
        "name": l.name,
        "email": l.email,
        "company": l.company,
        "industry": l.industry,
        "status": l.status,
        "lead_score": l.lead_score,
        "priority": l.priority,
        "confidence": l.confidence,
        "is_qualified": l.is_qualified,
        "email_subject": l.email_subject,
        "created_at": l.created_at.isoformat() if l.created_at else None,
    } for l in leads]

@router.put("/{lead_id}", response_model=dict)
async def update_lead(lead_id: int, lead_data: dict, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for key, value in lead_data.items():
        setattr(lead, key, value)
    db.commit()
    return {"message": "Lead updated successfully"}

@router.delete("/{lead_id}", response_model=dict)
async def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"message": "Lead deleted successfully"}
