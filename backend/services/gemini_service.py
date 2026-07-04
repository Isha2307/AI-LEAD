import re
import json
from backend.utils.logger import app_logger

class GeminiService:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GeminiService, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key: str = None, model_name: str = "gemini-2.5-flash"):
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
            name_match = re.search(r"Name:\s*([^\n]*)", user_prompt)
            name = name_match.group(1).strip() if name_match else "Daniel Peterson"
            
            company_match = re.search(r"Company:\s*([^\n]*)", user_prompt)
            company = company_match.group(1).strip() if company_match else "InnovateSolve"
            
            industry_match = re.search(r"Industry:\s*([^\n]*)", user_prompt)
            industry = industry_match.group(1).strip() if industry_match else "SaaS"
            
            emp_match = re.search(r"Employee Count:\s*([^\n]*)", user_prompt)
            emp_count_str = emp_match.group(1).strip() if emp_match else "280"
            try:
                emp_count = int(emp_count_str)
            except ValueError:
                emp_count = 50

            msg_match = re.search(r"Lead Message:\s*(.*)", user_prompt, re.DOTALL)
            lead_message = msg_match.group(1).strip() if msg_match else ""

            # Check if there is budget or timeline info in message
            budget = "Under $50K"
            estimated_budget = "Under $50K"
            if "180" in lead_message or "150" in lead_message or "120" in lead_message or "100" in lead_message or "enterprise" in lead_message.lower():
                budget = "$100K-$200K (Enterprise budget)"
                estimated_budget = "$100K-$200K (Enterprise budget)"
            elif "50" in lead_message or "mid" in lead_message.lower():
                budget = "$50K-$100K (Mid-Market budget)"
                estimated_budget = "$50K-$100K (Mid-Market budget)"

            timeline = "Within 6 months"
            decision_timeline = "Within 6 months"
            if "asap" in lead_message.lower() or "immediate" in lead_message.lower() or "this quarter" in lead_message.lower() or "q3" in lead_message.lower() or "q4" in lead_message.lower() or "immediate" in lead_message.lower():
                timeline = "Immediate (Q3/Q4 implementation)"
                decision_timeline = "Immediate (Q3/Q4 implementation)"
            
            urgency = "High" if "immediate" in timeline.lower() or "immediate" in lead_message.lower() or "asap" in lead_message.lower() else "Medium"
            
            company_size = "Enterprise" if emp_count >= 500 else ("Mid-Market" if emp_count >= 100 else "SMB")

            # Extract any research findings that were appended to the lead message
            company_research = ""
            research_match = re.search(r"Company Research Findings:\s*(.*)", lead_message, re.DOTALL)
            if research_match:
                company_research = research_match.group(1).strip()
            
            mock_data = {
                "summary": f"Inbound request from {name} at {company} seeking sales pipeline automation and scoring systems.",
                "requirement": "AI-powered CRM lead scoring pipeline implementation.",
                "budget": budget,
                "timeline": timeline,
                "urgency": urgency,
                "company_size": company_size,
                "industry": industry,
                "pain_points": [
                    "Manual review bottlenecks in sales queue",
                    "Lead conversion rates dropping due to slow response",
                    "Lack of priority scoring logic"
                ],
                "company_name": company,
                "technology_stack": ["FastAPI", "MongoDB", "React", "Python"],
                "estimated_budget": estimated_budget,
                "decision_timeline": decision_timeline,
                "key_decision_makers": ["VP of Operations", "Sales Operations Lead"],
                "engagement_level": urgency,
                "company_research": company_research
            }
            return json.dumps(mock_data)
            
        elif "sales lead scoring agent" in system_prompt.lower():
            # Lead Scoring
            # Let's extract budget, timeline, and urgency from user_prompt to calculate score dynamically!
            score = 65  # Default baseline
            reasoning = []
            
            budget_match = re.search(r"Budget:\s*([^\n]*)", user_prompt)
            budget = budget_match.group(1).lower() if budget_match else ""
            
            timeline_match = re.search(r"Timeline:\s*([^\n]*)", user_prompt)
            timeline = timeline_match.group(1).lower() if timeline_match else ""
            
            urgency_match = re.search(r"Urgency:\s*([^\n]*)", user_prompt)
            urgency = urgency_match.group(1).lower() if urgency_match else ""

            # Check budget score
            if "100k" in budget or "enterprise" in budget or "200k" in budget or "150k" in budget or "180k" in budget:
                score += 15
                reasoning.append("Substantial enterprise budget range identified ($100k+)")
            elif "50k" in budget or "mid" in budget:
                score += 10
                reasoning.append("Solid mid-market budget range identified")
            else:
                score += 5
                reasoning.append("No explicit large budget mentioned")

            # Check timeline score
            if "asap" in timeline or "immediate" in timeline or "q3" in timeline or "q4" in timeline:
                score += 15
                reasoning.append("Immediate to short-term implementation timeline")
            else:
                score += 5
                reasoning.append("Medium-term timeline specified")

            # Check urgency score
            if "high" in urgency:
                score += 5
                reasoning.append("High deal urgency level reported")
            else:
                score += 2

            # Let's cap score at 99
            lead_score = min(score, 99)
            priority = "Hot" if lead_score >= 80 else ("Warm" if lead_score >= 50 else "Cold")

            mock_data = {
                "lead_score": lead_score,
                "score": lead_score,
                "priority": priority,
                "confidence": 95,
                "reasoning": reasoning
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

    def generate_content_with_search(self, system_prompt: str, user_prompt: str) -> str:
        if self.is_mock:
            app_logger.debug("Generating mock Gemini response with search...")
            # Extract company name
            company = "NexaSoft Technologies"
            company_match = re.search(r"company:\s*'([^']+)'", user_prompt, re.IGNORECASE)
            if company_match:
                company = company_match.group(1).strip()
            
            # Extract name
            contact = "Sarah Mitchell"
            contact_match = re.search(r"contact:\s*'([^']+)'", user_prompt, re.IGNORECASE)
            if contact_match:
                contact = contact_match.group(1).strip()

            return (
                f"Research Summary for {company}:\n"
                f"• Company Profile: {company} is a leading enterprise player offering innovative SaaS products and customized business solutions.\n"
                f"• Approximate Company Size: 100-500 employees (Mid-Market to Large Enterprise).\n"
                f"• Main Industry: Software development and technology consulting services.\n"
                f"• Key Employee Roles Detected: {contact} (Executive Director / VP of Operations), who manages strategic digital transformation initiatives.\n"
                f"• Online Presence & Status: Strong reputation for quality integrations and modern backend pipelines.\n"
                f"• Tech Stack: Python, FastAPI, Node.js, React, AWS, Docker."
            )
            
        try:
            import google.generativeai as genai
            # Try to initialize GenerativeModel with system instruction and Google Search grounding tool
            app_logger.info(f"Gemini Service: Generating content with Google Search grounding for model {self.model_name}")
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt,
                tools=[{"google_search": {}}]
            )
            response = model.generate_content(user_prompt)
            return response.text
        except Exception as e:
            app_logger.warning(f"Failed calling Gemini with Google Search tool: {e}. Falling back to standard generate_content.")
            return self.generate_content(system_prompt, user_prompt)
