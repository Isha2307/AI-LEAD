from backend.config.settings import get_settings
from backend.services.gemini_service import GeminiService
from backend.agents.lead_analyzer import LeadAnalysisAgent
from backend.agents.lead_scorer import LeadScoringAgent
from backend.agents.email_generator import EmailGenerationAgent

# Initialize configurations and service singleton
settings = get_settings()
gemini_service = GeminiService(api_key=settings.GEMINI_API_KEY, model_name=settings.GEMINI_MODEL)

# Initialize agent singletons
lead_analyzer_agent = LeadAnalysisAgent(gemini_service=gemini_service)
lead_analysis_agent = lead_analyzer_agent  # Alias used in example_integrated_workflow.py

lead_scoring_agent = LeadScoringAgent(gemini_service=gemini_service)

email_generator_agent = EmailGenerationAgent(gemini_service=gemini_service)

__all__ = [
    "LeadAnalysisAgent",
    "LeadScoringAgent",
    "EmailGenerationAgent",
    "lead_analyzer_agent",
    "lead_analysis_agent",
    "lead_scoring_agent",
    "email_generator_agent",
]
