from backend.agents import lead_analyzer_agent, lead_scoring_agent, email_generator_agent

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

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
from backend.config.settings import get_settings

settings = get_settings()
router = APIRouter(tags=["leads"])

def serialize_lead(lead_doc) -> dict:
    if not lead_doc:
        return {}
    d = dict(lead_doc)
    if "_id" in d:
        d["id"] = str(d["_id"])
        del d["_id"]
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.isoformat()
    return d

# Helper function to update/save database lead record
def save_or_update_lead(db, email: str, update_data: dict):
    if settings.IS_MONGODB:
        now = datetime.utcnow()
        db.leads.update_one(
            {"email": email},
            {
                "$set": {**update_data, "updated_at": now},
                "$setOnInsert": {"created_at": now}
            },
            upsert=True
        )
        return serialize_lead(db.leads.find_one({"email": email}))
    else:
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
        if settings.IS_MONGODB:
            db.leads.update_one(
                {"company": request.company},
                {"$set": {"email_subject": email_result.subject, "email_body": email_result.email}}
            )
        else:
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
async def create_lead(lead_data: dict, db = Depends(get_db)):
    email = lead_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    save_or_update_lead(db, email, lead_data)
    return {"message": "Lead created successfully"}

@router.get("/qualified/list", response_model=List[dict])
async def list_qualified_leads(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    if settings.IS_MONGODB:
        leads = list(db.leads.find({"is_qualified": True}).skip(skip).limit(limit))
        return [serialize_lead(l) for l in leads]
    else:
        leads = db.query(Lead).filter(Lead.is_qualified == True).offset(skip).limit(limit).all()
        return [{
            "id": l.id,
            "name": l.name,
            "email": l.email,
            "company": l.company,
            "qualification_score": l.qualification_score
        } for l in leads]

@router.get("/{lead_id}", response_model=dict)
async def get_lead(lead_id: str, db = Depends(get_db)):
    if settings.IS_MONGODB:
        query = {}
        try:
            query = {"_id": ObjectId(lead_id)}
        except Exception:
            try:
                query = {"id": int(lead_id)}
            except Exception:
                query = {"id": lead_id}
        lead = db.leads.find_one(query)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        return serialize_lead(lead)
    else:
        try:
            lid = int(lead_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid lead ID format for SQLite")
        lead = db.query(Lead).filter(Lead.id == lid).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
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
async def list_leads(skip: int = 0, limit: int = 10, status: Optional[str] = None, db = Depends(get_db)):
    if settings.IS_MONGODB:
        query = {}
        if status:
            query["status"] = status
        leads = list(db.leads.find(query).skip(skip).limit(limit))
        return [serialize_lead(l) for l in leads]
    else:
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
async def update_lead(lead_id: str, lead_data: dict, db = Depends(get_db)):
    if settings.IS_MONGODB:
        query = {}
        try:
            query = {"_id": ObjectId(lead_id)}
        except Exception:
            try:
                query = {"id": int(lead_id)}
            except Exception:
                query = {"id": lead_id}
        res = db.leads.update_one(query, {"$set": lead_data})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        return {"message": "Lead updated successfully"}
    else:
        try:
            lid = int(lead_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid lead ID format for SQLite")
        lead = db.query(Lead).filter(Lead.id == lid).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        for key, value in lead_data.items():
            setattr(lead, key, value)
        db.commit()
        return {"message": "Lead updated successfully"}

@router.delete("/{lead_id}", response_model=dict)
async def delete_lead(lead_id: str, db = Depends(get_db)):
    if settings.IS_MONGODB:
        query = {}
        try:
            query = {"_id": ObjectId(lead_id)}
        except Exception:
            try:
                query = {"id": int(lead_id)}
            except Exception:
                query = {"id": lead_id}
        res = db.leads.delete_one(query)
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        return {"message": "Lead deleted successfully"}
    else:
        try:
            lid = int(lead_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid lead ID format for SQLite")
        lead = db.query(Lead).filter(Lead.id == lid).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        db.delete(lead)
        db.commit()
        return {"message": "Lead deleted successfully"}

