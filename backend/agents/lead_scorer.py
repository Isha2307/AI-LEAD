# Import agents first to resolve Python 3.14 C-extension initialization order conflict
from backend.services.gemini_service import GeminiService
from backend.schemas.lead_schema import LeadAnalysisResult, LeadScoringResult, LeadScoringRequest
from backend.prompts.lead_prompts import get_lead_scoring_prompt, SYSTEM_PROMPT_LEAD_SCORER
from backend.utils.logger import app_logger

import json
from typing import List, Dict, Any
from pydantic import BaseModel

class LeadScoringAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    def get_priority_from_score(self, score: Any) -> str:
        # Extrapolate numeric score from various input formats
        if hasattr(score, "lead_score"):
            score_val = score.lead_score
        elif isinstance(score, dict):
            score_val = score.get("lead_score", score.get("score", 0))
        else:
            try:
                score_val = int(score)
            except Exception:
                score_val = 0
                
        if score_val >= 80:
            return "Hot"
        elif score_val >= 50:
            return "Warm"
        else:
            return "Cold"

    def get_action_recommendation(self, score: Any) -> str:
        priority = self.get_priority_from_score(score)
        if priority == "Hot":
            return "Contact within 24 hours. Propose immediate meeting."
        elif priority == "Warm":
            return "Follow up within 3-5 days. Send case study or invite to webinar."
        else:
            return "Add to nurture campaign. Send monthly updates."

    def score_lead(
        self,
        analysis_data: Any = None,
        name: str = None,
        email: str = None,
        company: str = None,
        industry: str = None,
        employee_count: int = None,
        lead_message: str = None,
        analysis: Any = None,
    ) -> LeadScoringResult:
        app_logger.info("LeadScoringAgent: Scoring lead")
        
        # Determine arguments
        # In example_integrated_workflow, score_lead receives the Pydantic analysis object as the first parameter
        if analysis_data is not None:
            if isinstance(analysis_data, (dict, BaseModel)):
                analysis = analysis_data
            elif isinstance(analysis_data, str):
                try:
                    analysis = json.loads(analysis_data)
                except Exception:
                    pass

        # If lead information was not provided separately, try to extract it from analysis
        if name is None:
            name = "Unknown"
            email = "unknown@company.com"
            if isinstance(analysis, BaseModel):
                company = getattr(analysis, "company_name", getattr(analysis, "company", "Unknown"))
                industry = getattr(analysis, "industry", "Unknown")
            elif isinstance(analysis, dict):
                company = analysis.get("company_name", analysis.get("company", "Unknown"))
                industry = analysis.get("industry", "Unknown")
            else:
                company = "Unknown"
                industry = "Unknown"
            employee_count = 1
            lead_message = "No lead message provided."

        # Parse analysis into dictionary
        if isinstance(analysis, BaseModel):
            analysis_dict = analysis.model_dump()
        elif isinstance(analysis, dict):
            analysis_dict = analysis
        else:
            raise ValueError("Invalid analysis data. Must be dict or BaseModel.")

        # Ensure schemas map correctly
        analysis_obj = LeadAnalysisResult(**analysis_dict)
        
        lead_dict = {
            "name": name,
            "email": email,
            "company": company,
            "industry": industry,
            "employee_count": employee_count,
            "lead_message": lead_message
        }

        # Generate User prompt
        user_prompt = get_lead_scoring_prompt(lead_dict, analysis_obj.model_dump())

        # Call Gemini API
        response_text = self.gemini_service.generate_content(SYSTEM_PROMPT_LEAD_SCORER, user_prompt)

        # Extract and parse response
        response_dict = self.gemini_service.extract_json_from_text(response_text)

        try:
            result = LeadScoringResult(**response_dict)
            app_logger.info(f"LeadScoringAgent: Successfully scored lead with score: {result.lead_score}")
            return result
        except Exception as e:
            app_logger.error(f"LeadScoringAgent: Schema parsing failed: {e}")
            raise ValueError(f"Schema mapping failed: {str(e)}")

    def batch_score_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        app_logger.info(f"LeadScoringAgent: Starting batch scoring for {len(leads)} leads")
        results = []
        for item in leads:
            try:
                lead = item.get("lead", item)
                analysis = item.get("analysis")
                scoring = self.score_lead(
                    name=lead.get("name"),
                    email=lead.get("email"),
                    company=lead.get("company"),
                    industry=lead.get("industry"),
                    employee_count=lead.get("employee_count"),
                    lead_message=lead.get("lead_message"),
                    analysis=analysis
                )
                results.append({
                    "status": "success",
                    "lead": lead,
                    "analysis": analysis,
                    "scoring": scoring.model_dump()
                })
            except Exception as e:
                app_logger.error(f"LeadScoringAgent: Failed to score batch lead: {e}")
                results.append({
                    "status": "failed",
                    "lead": lead,
                    "error": str(e)
                })
        return results
