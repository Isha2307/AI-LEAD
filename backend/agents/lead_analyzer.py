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

    def parse_email(self, email_content: str) -> Dict[str, Any]:
        app_logger.info("LeadAnalysisAgent: Parsing raw email content")
        system_prompt = """You are an expert sales operations analyst.
Your job is to parse raw sales inquiry or prospect email content and extract structured lead info.
You must extract:
1. Contact Name (sender's name or person mentioned as contact)
2. Contact Email (sender's email or email mentioned)
3. Company Name (sender's company)
4. Industry (if mentioned or inferred from company name / content)
5. Estimated Employee Count / Company Size (if mentioned or inferred, default to 50 if unknown)
6. Raw message summary or needs/requirements (as the lead_message)

CRITICAL: Return ONLY a valid, raw JSON object. Do NOT wrap the JSON in markdown code blocks, do not write preambles, and do not write explanations.
Your response must start with '{' and end with '}' and be valid JSON."""

        user_prompt = f"""Raw Email Content:
\"\"\"
{email_content}
\"\"\"

Extract fields into this JSON structure:
{{
  "name": "Full Name",
  "email": "email@example.com",
  "company": "Company Name",
  "industry": "Industry Sector",
  "employee_count": 50,
  "lead_message": "Extracted requirements or inquiry context from the email"
}}"""
        if self.gemini_service.is_mock:
            # Simple heuristic/mock extraction
            import re
            
            # 1. Extract email
            email = "unknown@company.com"
            email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", email_content)
            if email_match:
                email = email_match.group(0).strip()
            
            # 2. Extract name
            name = "Unknown"
            # Try to match From: Name <email>
            from_match = re.search(r"From:\s*([^<\n]+)", email_content)
            if from_match:
                name = from_match.group(1).replace('"', '').replace("'", "").strip()
            else:
                # Try to extract name from signature block
                sig_match = re.search(r"(?:regards|sincerely|best|thanks|thank you),?\s*\n+([A-Z][a-zA-Z'\s]+)", email_content, re.IGNORECASE)
                if sig_match:
                    name = sig_match.group(1).strip().split('\n')[0].strip()
            
            # 3. Extract company
            company = "Unknown Company"
            # Look for "at CompanyName" or company indicators
            comp_match = re.search(r"(?:at|from)\s+([A-Z][a-zA-Z0-9\s]{2,40}\s+(?:Solutions|Technologies|Software|Corp|Inc|Co\.|LLC|Group|Consulting))", email_content)
            if comp_match:
                company = comp_match.group(1).strip()
            else:
                # Use email domain as fallback
                domain_parts = email.split('@')
                if len(domain_parts) > 1:
                    domain = domain_parts[1].split('.')[0]
                    company = domain.replace('-', ' ').title()
            
            # 4. Extract employee count
            employee_count = 50
            emp_match = re.search(r"(\d+)\s*(?:employees|people|staff|workers)", email_content, re.IGNORECASE)
            if emp_match:
                employee_count = int(emp_match.group(1))
            else:
                emp_match_2 = re.search(r"(?:size|count) is (?:about|around)?\s*(\d+)", email_content, re.IGNORECASE)
                if emp_match_2:
                    employee_count = int(emp_match_2.group(1))
            
            # 5. Extract Industry
            industry = "Technology"
            for ind in ["SaaS", "Software", "Workflow", "Healthcare", "Consulting", "Finance", "Retail", "Manufacturing"]:
                if ind.lower() in email_content.lower():
                    industry = ind
                    break
                    
            # 6. Extract lead message / requirement
            lead_message = email_content
            # Try to grab the body after greeting
            body_match = re.search(r"(?:Dear|Hi|Hello)[^\n]*\n+(.*)", email_content, re.DOTALL)
            if body_match:
                lead_message = body_match.group(1).strip()
            
            # Limit message length
            if len(lead_message) > 500:
                lead_message = lead_message[:500] + "..."
            
            return {
                "name": name,
                "email": email,
                "company": company,
                "industry": industry,
                "employee_count": employee_count,
                "lead_message": lead_message
            }

        response_text = self.gemini_service.generate_content(system_prompt, user_prompt)
        response_dict = self.gemini_service.extract_json_from_text(response_text)
        return response_dict

    def research_company(self, company_name: str, employee_name: str = None) -> str:
        app_logger.info(f"LeadAnalysisAgent: Researching company: {company_name}")
        system_prompt = """You are an expert market researcher and business intelligence analyst.
Your job is to search for and compile public information about a target company and its key team members.
You must find:
1. What the company does (industry, product/service, business model).
2. Size, scale, and general market presence.
3. Information about key leadership or the specific contact if mentioned.
4. Technologies they are likely using or interested in.

Provide a concise, professional research summary formatted as bullet points."""

        user_prompt = f"Perform business research on the company: '{company_name}'"
        if employee_name:
            user_prompt += f" and target contact: '{employee_name}'"

        response_text = self.gemini_service.generate_content_with_search(system_prompt, user_prompt)
        return response_text

    def analyze_email_lead(self, email_content: str) -> Tuple[Dict[str, Any], LeadAnalysisResult]:
        # Step 1: Parse Email
        parsed_data = self.parse_email(email_content)
        
        # Step 2: Research Company
        company = parsed_data.get("company", "Unknown")
        name = parsed_data.get("name", "Unknown")
        research_notes = self.research_company(company, name)
        
        # Step 3: Standard Lead Analysis with Enriched Context
        enriched_message = (
            f"Lead Inquiry Message:\n{parsed_data.get('lead_message')}\n\n"
            f"Company Research Findings:\n{research_notes}"
        )
        
        analysis = self.analyze_lead(
            name=parsed_data.get("name"),
            email=parsed_data.get("email"),
            company=parsed_data.get("company"),
            industry=parsed_data.get("industry"),
            employee_count=parsed_data.get("employee_count"),
            lead_message=enriched_message
        )
        
        # Set the research on the analysis result object
        analysis.company_research = research_notes
        
        return parsed_data, analysis
