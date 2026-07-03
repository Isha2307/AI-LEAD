import re
import json
from backend.utils.logger import app_logger

class GeminiService:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GeminiService, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key: str = None, model_name: str = "gemini-pro"):
        if not hasattr(self, "initialized"):
            self.api_key = api_key
            self.model_name = model_name
            
            # Check if using a mock/placeholder API key
            self.is_mock = (
                not api_key or 
                "your_gemini_api_key" in api_key or 
                "sk-proj-xxxxx" in api_key or 
                api_key.strip() == ""
            )
            
            if self.is_mock:
                app_logger.warning("Gemini Service: Running in MOCK MODE because no valid GEMINI_API_KEY was provided.")
                self.model = None
                self.client_connected = False
            else:
                try:
                    # Lazy import to avoid loading C-extensions (like grpcio) in mock mode
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel(model_name=self.model_name)
                    self.client_connected = True
                    app_logger.info(f"Gemini Service: Initialized successfully with model: {self.model_name}")
                except Exception as e:
                    app_logger.error(f"Gemini Service: Failed to initialize Gemini API: {str(e)}")
                    self.is_mock = True
                    self.model = None
                    self.client_connected = False
            self.initialized = True
            
    def generate_content(self, system_prompt: str, user_prompt: str) -> str:
        if self.is_mock:
            return self._generate_mock_content(system_prompt, user_prompt)
            
        try:
            import google.generativeai as genai
            # Try newer SDK with system_instruction support
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            response = model.generate_content(user_prompt)
            return response.text
        except Exception as e:
            app_logger.warning(f"Failed calling Gemini with system_instruction: {e}. Falling back to combined prompt.")
            try:
                import google.generativeai as genai
                # Fallback to combined prompt on older SDKs
                model = genai.GenerativeModel(model_name=self.model_name)
                combined = f"{system_prompt}\n\nUser Request:\n{user_prompt}"
                response = model.generate_content(combined)
                return response.text
            except Exception as ex:
                app_logger.error(f"Gemini service execution failure: {ex}")
                raise RuntimeError(f"Gemini API call failed: {str(ex)}") from ex

    def _generate_mock_content(self, system_prompt: str, user_prompt: str) -> str:
        app_logger.debug("Generating mock Gemini response...")
        
        # Determine the request type based on the prompts
        if "sales lead qualification analyst" in system_prompt.lower():
            # Lead Analysis
            company_match = re.search(r"Company:\s*(.*)", user_prompt)
            company = company_match.group(1).strip() if company_match else "TechCorp"
            
            industry_match = re.search(r"Industry:\s*(.*)", user_prompt)
            industry = industry_match.group(1).strip() if industry_match else "Technology"
            
            mock_data = {
                "summary": f"A mid-market company operating in the {industry} sector seeking to improve lead management.",
                "requirement": "AI-powered lead qualification and scoring pipeline implementation.",
                "budget": "$100K-$200K (Mid-Market budget)",
                "timeline": "ASAP (Q3 2024 implementation)",
                "urgency": "High",
                "company_size": "Mid-Market",
                "industry": industry,
                "pain_points": [
                    "Manual lead review takes too much time",
                    "Slow response times causing lost sales",
                    "Lack of automated priority scoring"
                ],
                "company_name": company,
                "technology_stack": ["FastAPI", "SQLite", "Pydantic", "Python"],
                "estimated_budget": "$100K-$200K (Mid-Market budget)",
                "decision_timeline": "ASAP (Q3 2024 implementation)",
                "key_decision_makers": ["Sales Operations Manager", "CTO"],
                "engagement_level": "High"
            }
            return json.dumps(mock_data)
            
        elif "sales lead scoring agent" in system_prompt.lower():
            # Lead Scoring
            mock_data = {
                "lead_score": 87,
                "score": 87,
                "priority": "Hot",
                "confidence": 92,
                "reasoning": [
                    "High urgency timeline (ASAP/Q3)",
                    "Substantial budget range ($100K-$200K)",
                    "3 critical pain points identified in operations"
                ]
            }
            return json.dumps(mock_data)
            
        elif "b2b sales copywriter" in system_prompt.lower():
            # Email Generation
            company_match = re.search(r"Company:\s*(.*)", user_prompt)
            company = company_match.group(1).strip() if company_match else "Prospect Corp"
            
            priority_match = re.search(r"Lead Priority:\s*(.*)", user_prompt)
            priority = priority_match.group(1).strip() if priority_match else "Warm"
            
            subject = f"Accelerating {company}'s Growth Trajectory"
            if priority == "Hot":
                subject = f"Next Steps: AI Lead Qualification for {company}"
                email_body = (
                    f"Hi there,\n\n"
                    f"I saw that your team at {company} is looking to automate your lead scoring. "
                    f"Given your immediate timeline and the pain points you mentioned around manual lead reviews, "
                    f"I wanted to reach out directly.\n\n"
                    f"We specialize in deploying custom FastAPI-based AI scoring agents that plug directly into CRM systems, "
                    f"helping teams cut manual review times in half. Since you're looking to move quickly, "
                    f"do you have 10 minutes tomorrow afternoon for a brief introductory call to see if we're a fit?\n\n"
                    f"Best regards,\nSales Team"
                )
            elif priority == "Warm":
                email_body = (
                    f"Hi there,\n\n"
                    f"I noticed {company} is currently evaluating sales automation options. "
                    f"Many mid-market companies in your sector face similar challenges with manual lead distribution. "
                    f"I've attached a brief case study showing how we helped a similar team automate lead scoring and boost sales productivity by 35%.\n\n"
                    f"I'd love to share some insights next week if you're open to it. Let me know if you have any availability.\n\n"
                    f"Warmly,\nSales Team"
                )
            else:
                email_body = (
                    f"Hi there,\n\n"
                    f"I wanted to share some insights on B2B lead generation trends that might be helpful for {company}. "
                    f"We recently compiled a guide on integrating LLM-based qualification. "
                    f"I've linked it below in case your team is exploring these tools.\n\n"
                    f"No pressure at all—feel free to reach out if you have any questions.\n\n"
                    f"Best,\nSales Team"
                )
                
            mock_data = {
                "subject": subject,
                "email": email_body
            }
            return json.dumps(mock_data)
            
        else:
            return "{}"

    def extract_json_from_text(self, text: str) -> dict:
        text = text.strip()
        if not text:
            raise ValueError("Empty response text from Gemini")
            
        # Try direct JSON parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
            
        # Try finding markdown code block
        markdown_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if markdown_match:
            try:
                return json.loads(markdown_match.group(1).strip())
            except json.JSONDecodeError:
                pass
                
        # Try finding brace match
        brace_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(1).strip())
            except json.JSONDecodeError:
                pass
                
        raise ValueError("Could not extract valid JSON from Gemini response")
