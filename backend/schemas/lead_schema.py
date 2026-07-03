from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import List, Optional, Literal, Any
from datetime import datetime

# ==========================================
# Lead Analysis Schemas
# ==========================================

class LeadAnalysisRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    company: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., min_length=1, max_length=100)
    employee_count: int = Field(..., ge=1)
    lead_message: str = Field(..., min_length=10)

    @model_validator(mode="before")
    @classmethod
    def map_incoming_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            # Map company_size to employee_count
            if "employee_count" not in values or values["employee_count"] is None:
                size_str = str(values.get("company_size", ""))
                if "500+" in size_str:
                    values["employee_count"] = 500
                elif "100-500" in size_str:
                    values["employee_count"] = 250
                elif "<50" in size_str or "50" in size_str:
                    values["employee_count"] = 20
                else:
                    values["employee_count"] = 100  # Default fallback
            
            # Map recent_activity / pain_points to lead_message
            if "lead_message" not in values or not values["lead_message"] or len(str(values["lead_message"])) < 10:
                msg_parts = []
                if "recent_activity" in values and values["recent_activity"]:
                    msg_parts.append(f"Recent Activity: {values['recent_activity']}")
                if "pain_points" in values and values["pain_points"]:
                    msg_parts.append(f"Pain Points: {values['pain_points']}")
                
                joined_msg = ". ".join(msg_parts)
                if len(joined_msg) >= 10:
                    values["lead_message"] = joined_msg
                else:
                    values["lead_message"] = "Exploring sales and AI qualification automation options."
            
            # Map industry
            if "industry" not in values or not values["industry"]:
                values["industry"] = "Technology"
                
            # Default for name / company
            if "name" not in values or not values["name"]:
                values["name"] = "Unknown"
            if "company" not in values or not values["company"]:
                values["company"] = "Unknown"
                
        return values


class LeadAnalysisResult(BaseModel):
    summary: str = Field(default="")
    requirement: str = Field(default="")
    budget: str = Field(default="")
    timeline: str = Field(default="")
    urgency: str = Field(default="")
    company_size: str = Field(default="")
    industry: str = Field(default="")
    pain_points: List[str] = Field(default_factory=list)

    # Fields for integrated workflow compatibility
    company_name: Optional[str] = None
    technology_stack: List[str] = Field(default_factory=list)
    estimated_budget: Optional[str] = None
    decision_timeline: Optional[str] = None
    key_decision_makers: List[str] = Field(default_factory=list)
    engagement_level: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def sync_integrated_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            # company_name <-> company
            if "company_name" not in values and "company" in values:
                values["company_name"] = values["company"]
            elif "company" not in values and "company_name" in values:
                values["company"] = values["company_name"]
            
            # estimated_budget <-> budget
            if "estimated_budget" not in values and "budget" in values:
                values["estimated_budget"] = values["budget"]
            elif "budget" not in values and "estimated_budget" in values:
                values["budget"] = values["estimated_budget"]
                
            # decision_timeline <-> timeline
            if "decision_timeline" not in values and "timeline" in values:
                values["decision_timeline"] = values["timeline"]
            elif "timeline" not in values and "decision_timeline" in values:
                values["timeline"] = values["decision_timeline"]
        return values

class LeadAnalysisOutput(BaseModel):
    name: str
    email: str
    company: str
    analysis: LeadAnalysisResult
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# Lead Scoring Schemas
# ==========================================

class LeadScoringRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    company: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., min_length=1, max_length=100)
    employee_count: int = Field(..., ge=1)
    lead_message: str = Field(..., min_length=10)
    analysis: LeadAnalysisResult

class LeadScoringResult(BaseModel):
    lead_score: int
    score: Optional[int] = None
    priority: Literal["Hot", "Warm", "Cold"]
    confidence: int
    reasoning: List[str]

    @model_validator(mode="before")
    @classmethod
    def sync_scores(cls, values: Any) -> Any:
        if isinstance(values, dict):
            lead_score = values.get("lead_score")
            score = values.get("score")
            if lead_score is not None and score is None:
                values["score"] = lead_score
            elif score is not None and lead_score is None:
                values["lead_score"] = score
        return values

class LeadScoringOutput(BaseModel):
    name: str
    email: str
    company: str
    analysis: LeadAnalysisResult
    scoring: LeadScoringResult
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# Email Generation Schemas
# ==========================================

class EmailGenerationRequest(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    requirement: str = Field(..., min_length=10)
    budget: str = Field(..., min_length=1, max_length=100)
    timeline: str = Field(..., min_length=1, max_length=100)
    priority: Literal["Hot", "Warm", "Cold"]

class EmailGenerationResult(BaseModel):
    subject: str = Field(..., min_length=10, max_length=200)
    email: str = Field(..., min_length=50)

class EmailGenerationOutput(BaseModel):
    company: str
    requirement: str
    priority: str
    email_content: EmailGenerationResult
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
