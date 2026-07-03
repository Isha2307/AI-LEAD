from typing import Dict, Any, Tuple
from backend.schemas.lead_schema import LeadAnalysisRequest, EmailGenerationRequest

SYSTEM_PROMPT_LEAD_ANALYST = """You are an expert sales lead qualification analyst.
Your job is to analyze incoming sales lead information and extract key insights.
You must categorize the lead's urgency, budget, timeline, company size, industry, and pain points.

CRITICAL: You must return ONLY a valid, raw JSON object. Do NOT wrap the JSON in markdown code blocks (e.g. do not use ```json ... ```), do not write any preambles, and do not provide any postscript explanation.
Your response must start with '{' and end with '}' and be valid JSON."""

SYSTEM_PROMPT_LEAD_SCORER = """You are an expert sales lead scoring agent.
Your job is to evaluate a sales lead based on their basic information and qualification analysis.
You must compute a score from 0 to 100, categorize the priority (Hot, Warm, Cold), assess your confidence (0-100), and list the reasons.

CRITICAL: You must return ONLY a valid, raw JSON object. Do NOT wrap the JSON in markdown code blocks, do not write any preambles, and do not provide any postscript explanation.
Your response must start with '{' and end with '}' and be valid JSON."""

SYSTEM_PROMPT_FOLLOW_UP = """You are an expert B2B sales copywriter with 15+ years of experience helping enterprise and mid-market companies implement AI solutions.
Your emails are:
• Professional yet warm and personable
• Value-focused, not sales-pitchy
• Specific to the prospect's stated needs
• Customized by lead priority level
• Compelling but never pushy

Your goal is to initiate meaningful B2B sales conversations, not hard-sell.

CRITICAL: You must return ONLY a valid, raw JSON object with "subject" and "email" fields. Do NOT wrap the JSON in markdown code blocks, do not write any preambles, and do not provide any postscript explanation."""


def get_lead_analysis_prompt(lead_data: Dict[str, Any]) -> str:
    return f"""Analyze the following sales lead:

Name: {lead_data.get('name')}
Email: {lead_data.get('email')}
Company: {lead_data.get('company')}
Industry: {lead_data.get('industry')}
Employee Count: {lead_data.get('employee_count')}
Lead Message: {lead_data.get('lead_message')}

Extract these specific insights and return a JSON object with this structure:
{{
  "summary": "2-3 sentence overview of who they are and what they want.",
  "requirement": "Specific need or system requested.",
  "budget": "Budget range or level mentioned or implied.",
  "timeline": "Timeline/urgency mentioned or implied.",
  "urgency": "High, Medium, or Low",
  "company_size": "Enterprise, Mid-Market, SMB, or Startup",
  "industry": "Industry sector classification.",
  "pain_points": ["List", "of", "pain", "points", "identified"],
  "company_name": "{lead_data.get('company')}",
  "technology_stack": ["Potential", "technologies", "mentioned"],
  "estimated_budget": "Same as budget field.",
  "decision_timeline": "Same as timeline field.",
  "key_decision_makers": ["Roles", "implied", "like", "Sales Director"],
  "engagement_level": "High, Medium, or Low"
}}"""


def validate_and_format_analysis_prompt(lead_data: Dict[str, Any]) -> Tuple[str, str]:
    try:
        # Validate data
        req = LeadAnalysisRequest(**lead_data)
        validated_dict = req.model_dump()
    except Exception as e:
        raise ValueError(f"Validation failed: {str(e)}")
    
    user_prompt = get_lead_analysis_prompt(validated_dict)
    return SYSTEM_PROMPT_LEAD_ANALYST, user_prompt


def get_lead_scoring_prompt(lead_data: Dict[str, Any], analysis_data: Dict[str, Any]) -> str:
    return f"""Evaluate the lead and compute a qualification score from 0 to 100 based on the following information:

Lead Profile:
Name: {lead_data.get('name')}
Email: {lead_data.get('email')}
Company: {lead_data.get('company')}
Industry: {lead_data.get('industry')}
Employee Count: {lead_data.get('employee_count')}
Message: {lead_data.get('lead_message')}

Analysis Results:
Summary: {analysis_data.get('summary')}
Requirement: {analysis_data.get('requirement')}
Budget: {analysis_data.get('budget')}
Timeline: {analysis_data.get('timeline')}
Urgency: {analysis_data.get('urgency')}
Pain Points: {analysis_data.get('pain_points')}

SCORING GUIDELINES:
- Budget: 0 to 25 points. Enterprise/large budget ($100k+) gets 25, mid-market gets 15, low/no budget gets 0.
- Timeline: 0 to 25 points. Immediate gets 25, 3-6 months gets 15, longer gets 0.
- Urgency: 0 to 25 points. High gets 25, Medium gets 15, Low gets 0.
- Pain Points: 0 to 20 points. 3+ pain points gets 20, 1-2 gets 10, none gets 0.

Priority levels:
- 80-100: Hot 🔥
- 50-79: Warm 🔶
- 0-49: Cold ❄️

Return a JSON object with this exact structure:
{{
  "lead_score": 85,
  "score": 85,
  "priority": "Hot",
  "confidence": 90,
  "reasoning": [
    "Short timeline (ASAP)",
    "Identified budget is substantial",
    "3 pain points identified"
  ]
}}"""


def get_email_generation_prompt(
    company: str,
    requirement: str,
    budget: str,
    timeline: str,
    priority: str
) -> str:
    # Determine style/guidance based on priority
    if priority == "Hot":
        guidance = "Tone: Urgent and action-oriented. Show that you can move fast. CTA: Propose an immediate next step (e.g. meeting tomorrow or this week)."
    elif priority == "Warm":
        guidance = "Tone: Consultative and educational. Offer case study or vertical business insights. CTA: Invite them to a conversation next week."
    else:
        guidance = "Tone: Helpful and value-first. Lead with value/insights. CTA: Soft, no pressure outreach."

    return f"""Generate a personalized sales follow-up email for this prospect:

Company: {company}
Stated Needs/Requirement: {requirement}
Budget Range: {budget}
Timeline: {timeline}
Lead Priority: {priority}

{guidance}

Return ONLY a valid JSON object:
{{
  "subject": "Compelling subject line under 70 characters",
  "email": "Professional email body of 150-250 words, with appropriate spacing and line breaks"
}}"""


def validate_and_format_email_prompt(email_data: Dict[str, Any]) -> Tuple[str, str]:
    try:
        req = EmailGenerationRequest(**email_data)
        validated_dict = req.model_dump()
    except Exception as e:
        raise ValueError(f"Validation failed: {str(e)}")
        
    user_prompt = get_email_generation_prompt(
        company=validated_dict.get("company", ""),
        requirement=validated_dict.get("requirement", ""),
        budget=validated_dict.get("budget", ""),
        timeline=validated_dict.get("timeline", ""),
        priority=validated_dict.get("priority", "Cold")
    )
    return SYSTEM_PROMPT_FOLLOW_UP, user_prompt
