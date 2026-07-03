import json
from typing import List, Dict, Any, Tuple
from backend.services.gemini_service import GeminiService
from backend.schemas.lead_schema import LeadAnalysisRequest, LeadAnalysisResult
from backend.prompts.lead_prompts import validate_and_format_analysis_prompt
from backend.utils.logger import app_logger

class LeadAnalysisAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    def get_qualification_score(self, analysis: LeadAnalysisResult) -> Tuple[float, bool]:
        score = 0.0
        
        # 1. Budget Assessment (0-25 points)
        budget = getattr(analysis, "budget", "").lower()
        if "enterprise" in budget or "$100k" in budget or "200k" in budget or "300k" in budget or "500k" in budget:
            score += 25.0
        elif "$10k" in budget or "50k" in budget or "mid-market" in budget or "medium" in budget:
            score += 15.0
            
        # 2. Timeline Assessment (0-25 points)
        timeline = getattr(analysis, "timeline", "").lower()
        if "immediate" in timeline or "asap" in timeline or "this quarter" in timeline or "q2" in timeline or "q3" in timeline or "q4" in timeline or "60 days" in timeline:
            score += 25.0
        elif "3-6 months" in timeline or "medium" in timeline or "mid-term" in timeline:
            score += 15.0
            
        # 3. Urgency Assessment (0-25 points)
        urgency = getattr(analysis, "urgency", "").lower()
        if "high" in urgency:
            score += 25.0
        elif "medium" in urgency:
            score += 15.0
            
        # 4. Pain Points Assessment (0-20 points)
        pain_points = getattr(analysis, "pain_points", [])
        if len(pain_points) >= 3:
            score += 20.0
        elif len(pain_points) >= 1:
            score += 10.0
            
        is_qualified = score >= 60.0
        return score, is_qualified

    def analyze_lead(
        self,
        lead_json: str = None,
        name: str = None,
        email: str = None,
        company: str = None,
        industry: str = None,
        employee_count: int = None,
        lead_message: str = None,
    ) -> LeadAnalysisResult:
        app_logger.info(f"LeadAnalysisAgent: Starting analysis for company: {company or 'unknown'}")
        
        # Handle positional or serialized JSON argument
        if lead_json is not None:
            try:
                # In case it is a JSON string
                data = json.loads(lead_json)
                name = data.get("name", name)
                email = data.get("email", email)
                company = data.get("company", company)
                industry = data.get("industry", industry)
                employee_count = data.get("employee_count", employee_count)
                lead_message = data.get("lead_message", lead_message)
            except Exception:
                raise ValueError("Invalid lead_json argument.")
                
        # Validate inputs via Pydantic schema
        lead_data = {
            "name": name,
            "email": email,
            "company": company,
            "industry": industry,
            "employee_count": employee_count,
            "lead_message": lead_message
        }
        
        # Validate and format prompts
        system_prompt, user_prompt = validate_and_format_analysis_prompt(lead_data)
        
        # Get response from Gemini
        response_text = self.gemini_service.generate_content(system_prompt, user_prompt)
        
        # Extract JSON and parse into result schema
        response_dict = self.gemini_service.extract_json_from_text(response_text)
        
        try:
            result = LeadAnalysisResult(**response_dict)
            app_logger.info(f"LeadAnalysisAgent: Successfully analyzed lead for company: {company}")
            return result
        except Exception as e:
            app_logger.error(f"LeadAnalysisAgent: Response schema validation failed: {e}")
            raise ValueError(f"Schema mapping failed: {str(e)}")

    def batch_analyze_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        app_logger.info(f"LeadAnalysisAgent: Starting batch analysis for {len(leads)} leads")
        results = []
        for lead in leads:
            try:
                analysis = self.analyze_lead(
                    name=lead.get("name"),
                    email=lead.get("email"),
                    company=lead.get("company"),
                    industry=lead.get("industry"),
                    employee_count=lead.get("employee_count"),
                    lead_message=lead.get("lead_message")
                )
                results.append({
                    "status": "success",
                    "lead": lead,
                    "analysis": analysis.model_dump()
                })
            except Exception as e:
                app_logger.error(f"LeadAnalysisAgent: Failed to analyze batch lead: {e}")
                results.append({
                    "status": "failed",
                    "lead": lead,
                    "error": str(e)
                })
        return results
