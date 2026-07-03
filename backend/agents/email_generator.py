from typing import List, Dict, Any
from backend.services.gemini_service import GeminiService
from backend.schemas.lead_schema import EmailGenerationResult
from backend.prompts.lead_prompts import validate_and_format_email_prompt, SYSTEM_PROMPT_FOLLOW_UP
from backend.utils.logger import app_logger

class EmailGenerationAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    def get_email_tone_guidance(self, priority: str) -> str:
        if priority == "Hot":
            return "Urgent, strong CTA, immediate next step"
        elif priority == "Warm":
            return "Consultative, educational, gentle CTA"
        else:
            return "Helpful, value-first, soft CTA"

    def customize_for_industry(self, industry: str) -> None:
        """Placeholder for future industry specific customization."""
        pass

    def generate_email(
        self,
        company: str,
        requirement: Any,
        budget: str,
        timeline: str,
        priority: str,
    ) -> EmailGenerationResult:
        app_logger.info(f"EmailGenerationAgent: Generating email for company: {company}")
        
        # Handle list format for requirement (e.g. if pain_points list is passed)
        if isinstance(requirement, list):
            requirement_str = ", ".join(requirement)
        else:
            requirement_str = str(requirement)

        email_data = {
            "company": company,
            "requirement": requirement_str,
            "budget": budget,
            "timeline": timeline,
            "priority": priority
        }

        # Validate and format prompt
        system_prompt, user_prompt = validate_and_format_email_prompt(email_data)

        # Call Gemini API
        response_text = self.gemini_service.generate_content(system_prompt, user_prompt)

        # Extract JSON
        response_dict = self.gemini_service.extract_json_from_text(response_text)

        try:
            result = EmailGenerationResult(**response_dict)
            app_logger.info(f"EmailGenerationAgent: Email successfully generated for {company}")
            return result
        except Exception as e:
            app_logger.error(f"EmailGenerationAgent: Response schema validation failed: {e}")
            raise ValueError(f"Schema mapping failed: {str(e)}")

    def batch_generate_emails(
        self,
        leads: List[Dict[str, str]]
    ) -> List[EmailGenerationResult]:
        app_logger.info(f"EmailGenerationAgent: Starting batch email generation for {len(leads)} leads")
        results = []
        for lead in leads:
            try:
                # Check for alternative key names
                company = lead.get("company", lead.get("company_name", ""))
                requirement = lead.get("requirement", lead.get("pain_points", ""))
                budget = lead.get("budget", lead.get("estimated_budget", ""))
                timeline = lead.get("timeline", lead.get("decision_timeline", ""))
                priority = lead.get("priority", "Cold")
                
                email_result = self.generate_email(
                    company=company,
                    requirement=requirement,
                    budget=budget,
                    timeline=timeline,
                    priority=priority
                )
                results.append(email_result)
            except Exception as e:
                app_logger.error(f"EmailGenerationAgent: Failed to generate batch email: {e}")
                # Append a fallback / error result to maintain list indices
                results.append(
                    EmailGenerationResult(
                        subject=f"Outreach to {lead.get('company', 'Prospect')}",
                        email=f"Error generating email: {str(e)}"
                    )
                )
        return results
