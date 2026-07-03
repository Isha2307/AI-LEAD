# Email Generation Agent - Comprehensive Documentation

## Overview

The **EmailGenerationAgent** is an AI-powered component of the Lead Qualification & Follow-up System that generates personalized, priority-aware professional B2B sales follow-up emails using Google's Gemini API.

This agent works seamlessly with the Lead Analysis Agent and Lead Scoring Agent to provide a complete lead qualification and outreach workflow:

1. **Lead Analysis** → Extracts structured data from lead information
2. **Lead Scoring** → Prioritizes leads (Hot/Warm/Cold) with confidence scores
3. **Email Generation** → Creates personalized follow-up emails tailored to priority

## Key Features

### ✅ Priority-Aware Email Generation
- **Hot Leads** 🔥: Urgent, action-oriented language with immediate CTAs
- **Warm Leads** 🔶: Consultative, interest-building tone with gentle CTAs
- **Cold Leads** ❄️: Educational, value-first approach with soft CTAs

### ✅ Professional Quality
- B2B sales expertise embedded in system prompts
- Professional yet personable tone
- 150-200 word target length
- Strong subject lines that stand out in inboxes

### ✅ Batch Processing
- Generate emails for multiple leads efficiently
- Error recovery for failed emails
- Batch operation logging and reporting

### ✅ Comprehensive Error Handling
- Input validation with specific error messages
- Graceful degradation on API errors
- Detailed logging for debugging

## Architecture

### Component Hierarchy

```
FastAPI Route (leads.py)
    ↓
EmailGenerationAgent (email_generator.py)
    ├── Validates inputs via validate_and_format_email_prompt()
    ├── Generates prompts from get_email_generation_prompt()
    └── Calls GeminiService for AI generation
        ├── System prompt (expert B2B copywriter)
        └── User prompt (priority-aware context + variables)
```

### Data Flow

```
HTTP Request
    ↓
EmailGenerationRequest (Pydantic validation)
    ↓
EmailGenerationAgent.generate_email()
    ├── Input validation
    ├── Prompt generation (with priority context)
    └── Gemini API call
        ├── JSON extraction
        └── Result validation
    ↓
EmailGenerationResult (subject + email body)
    ↓
EmailGenerationOutput (with metadata)
    ↓
HTTP Response (200/400/503/500)
```

## API Endpoint

### POST `/api/v1/leads/generate-email`

Generate a personalized follow-up email for a specific lead.

#### Request Schema: `EmailGenerationRequest`

```python
{
    "company": str,          # Company name (1-255 characters)
    "requirement": str,      # Business requirement (≥10 characters)
    "budget": str,          # Budget range (1-100 characters)
    "timeline": str,        # Timeline/urgency (1-100 characters)
    "priority": str         # Priority level: "Hot" | "Warm" | "Cold"
}
```

#### Response Schema: `EmailGenerationOutput`

```python
{
    "company": str,                           # Input company name
    "requirement": str,                       # Input requirement
    "priority": str,                          # Lead priority level
    "email_content": {
        "subject": str,                       # Email subject (10-200 chars)
        "email": str                          # Email body (≥50 chars)
    },
    "timestamp": str                          # ISO 8601 timestamp
}
```

#### Status Codes

| Code | Meaning | Notes |
|------|---------|-------|
| 200 | Success | Email generated successfully |
| 400 | Bad Request | Input validation failed |
| 503 | Service Unavailable | Gemini API not configured |
| 500 | Internal Error | Processing failure |

## Usage Examples

### Python Client

```python
from backend.agents import email_generator_agent

# Generate a single email
email_result = email_generator_agent.generate_email(
    company="TechCorp Solutions",
    requirement="Enterprise AI platform for customer support",
    budget="$200K-$500K",
    timeline="Q2 2024 (immediate)",
    priority="Hot"
)

print(f"Subject: {email_result.subject}")
print(f"Body: {email_result.email}")
```

### FastAPI HTTP Request

```bash
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "TechCorp Solutions",
    "requirement": "Enterprise AI platform for customer support",
    "budget": "$200K-$500K",
    "timeline": "Q2 2024 (immediate implementation)",
    "priority": "Hot"
  }'
```

### Python FastAPI Client

```python
import requests
import json

url = "http://localhost:8000/api/v1/leads/generate-email"

payload = {
    "company": "TechCorp Solutions",
    "requirement": "Enterprise AI platform for customer support",
    "budget": "$200K-$500K",
    "timeline": "Q2 2024 (immediate)",
    "priority": "Hot"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Subject: {result['email_content']['subject']}")
print(f"Email: {result['email_content']['email']}")
```

### Batch Email Generation

```python
from backend.agents import email_generator_agent

leads = [
    {
        "company": "Enterprise Corp",
        "requirement": "AI strategy for digital transformation",
        "budget": "$500K+",
        "timeline": "Q2 2024",
        "priority": "Hot"
    },
    {
        "company": "MidMarket Services",
        "requirement": "Process automation for back-office",
        "budget": "$100K-$150K",
        "timeline": "Q3 2024",
        "priority": "Warm"
    },
    {
        "company": "StartupXYZ",
        "requirement": "Low-cost AI tools exploration",
        "budget": "$15K-$25K",
        "timeline": "Unknown",
        "priority": "Cold"
    }
]

# Batch generate with error handling
results = email_generator_agent.batch_generate_emails(leads)

for lead, email_result in zip(leads, results):
    print(f"\n{lead['company']} ({lead['priority']}):")
    print(f"  Subject: {email_result.subject}")
    print(f"  Preview: {email_result.email[:100]}...")
```

## Priority Levels & Email Strategies

### 🔥 Hot Leads (Score: 80-100)

**Characteristics:**
- High purchase intent signals
- Large budget and short timeline
- Ready to move quickly

**Email Strategy:**
- **Tone**: Urgent and enthusiastic
- **Focus**: Immediate value and quick wins
- **CTA**: Strong call-to-action with clear next steps
- **Length**: Concise (150-200 words)
- **Goal**: Close meeting quickly

**Example Subject:**
> "Let's Talk About Your Q2 Customer Support Transformation"

**Example Approach:**
```
I appreciated learning about your Q2 timeline for implementing 
customer support automation. Given your $200K+ budget and the 
urgency in your timeline, I'd like to schedule a focused 30-minute 
call this week to walk through how we've helped similar enterprise 
clients achieve ROI in 60 days.

Are you available Tuesday or Wednesday morning?
```

### 🔶 Warm Leads (Score: 50-79)

**Characteristics:**
- Demonstrated interest
- Moderate budget and timeline
- Needs continued qualification

**Email Strategy:**
- **Tone**: Professional and consultative
- **Focus**: Education and building interest
- **CTA**: Gentle invitation to deeper conversation
- **Length**: Moderate (150-250 words)
- **Goal**: Nurture and qualify further

**Example Subject:**
> "How [Companies Similar to Them] Approach AI Automation"

**Example Approach:**
```
I've been following your company's growth in the data analytics 
space, and your Q3 timeline aligns well with how forward-thinking 
organizations are implementing AI solutions today.

I'd love to share a brief case study on how we helped similar 
mid-market companies achieve 40% operational efficiency improvements 
with their data integration strategy. Would a 20-minute call next 
week make sense?
```

### ❄️ Cold Leads (Score: 0-49)

**Characteristics:**
- Low immediate intent signals
- Uncertain budget and timeline
- Early-stage evaluation

**Email Strategy:**
- **Tone**: Helpful and value-focused
- **Focus**: Providing relevant insights upfront
- **CTA**: Soft, no pressure
- **Length**: Can be slightly longer (200+ words)
- **Goal**: Spark interest and add value

**Example Subject:**
> "The Future of AI in Your Industry [Research Insights]"

**Example Approach:**
```
I came across your company while researching innovative startups 
in the AI space. While I'm not sure if now's the right time for 
your team to explore AI tools, I thought you'd find this recent 
report valuable.

[Brief insight about industry trend]

If you ever want to explore how AI could accelerate your growth 
trajectory, I'm just an email away. No pressure—I'm here when 
you're ready.
```

## Prompt Engineering

### System Prompt Design

The agent uses an expert B2B copywriter persona in the system prompt:

```
You are an expert B2B sales copywriter with 15+ years of experience 
helping enterprise and mid-market companies implement AI solutions.

Your emails are:
• Professional yet warm and personable
• Value-focused, not sales-pitchy
• Specific to the prospect's stated needs
• Customized by lead priority level
• Compelling but never pushy

Your goal is to initiate meaningful conversations, not hard-sell.
```

### User Prompt Construction

The user prompt adapts based on lead priority:

**For Hot Leads:**
```
Generate a follow-up email for an enterprise prospect with:
• Strong buying signals - ready to move quickly
• Large budget ($200K+) and Q2 urgency
• Clear business need: [requirement]

Tone: Urgent and action-oriented. Express that you understand 
their timeline and can move quickly to deliver value.

Call-to-action: Propose a specific, immediate next step 
(meeting tomorrow/this week).
```

**For Warm Leads:**
```
Generate a follow-up email for a qualified prospect showing 
genuine interest:
• Budget: [budget], Timeline: [timeline]
• Business need: [requirement]
• At the investigation/evaluation stage

Tone: Consultative and educational. Build interest by showing 
you understand their business vertically and horizontally.

Call-to-action: Invite them to a conversation the following week, 
offering to share a relevant case study or insight.
```

**For Cold Leads:**
```
Generate a follow-up email for an early-stage prospect:
• Timeline: [timeline], Budget: [budget]
• Could have need for: [requirement]
• Uncertain evaluation stage

Tone: Helpful and value-first. Lead with insights, not needs. 
Make it valuable even if they don't respond.

Call-to-action: Soft—no pressure. Offer a resource or insight 
they can benefit from today.
```

### JSON Output Instruction

All prompts include explicit JSON formatting instruction:

```
Return ONLY a valid JSON object with this exact structure:
{
  "subject": "Compelling email subject line (under 70 chars)",
  "email": "Professional email body (150-250 words, with proper line breaks)"
}

Do NOT include any other text, explanations, or markdown formatting.
Just the JSON object.
```

## Implementation Details

### File Structure

```
backend/
├── agents/
│   ├── email_generator.py          # EmailGenerationAgent class
│   └── __init__.py                 # Exports
├── schemas/
│   ├── lead_schema.py              # Pydantic models
│   └── __init__.py                 # Exports
├── prompts/
│   ├── lead_prompts.py             # Prompt templates
│   └── __init__.py
├── services/
│   └── gemini_service.py           # GeminiService (pre-existing)
├── api/
│   └── routes/
│       ├── leads.py                # FastAPI endpoint
│       └── __init__.py
└── main.py                         # FastAPI app
```

### Key Classes

#### EmailGenerationAgent

```python
class EmailGenerationAgent:
    """Agent for generating personalized B2B sales emails."""
    
    def __init__(self, gemini_service: GeminiService):
        """Initialize with Gemini service."""
        self.gemini_service = gemini_service
    
    def generate_email(
        self,
        company: str,
        requirement: str,
        budget: str,
        timeline: str,
        priority: str,
    ) -> EmailGenerationResult:
        """Generate a single personalized email."""
        # Validation → Prompts → Gemini API → JSON extraction → Validation
    
    def batch_generate_emails(
        self,
        leads: List[Dict[str, str]]
    ) -> List[EmailGenerationResult]:
        """Generate emails for multiple leads with error recovery."""
    
    def get_email_tone_guidance(self, priority: str) -> str:
        """Get tone guidance for a specific priority level."""
    
    def customize_for_industry(self, industry: str) -> None:
        """Future enhancement for industry-specific customization."""
```

### Error Handling Strategy

```python
# Comprehensive error handling with specific types:

try:
    # Input validation with specific constraints
    validate_and_format_email_prompt(...)
    
    # Gemini API call with error recovery
    result = gemini_service.analyze_lead(...)
    
    # JSON extraction with multi-strategy fallback
    json_data = extract_json_from_text(result)
    
    # Pydantic validation
    email = EmailGenerationResult(**json_data)
    
    return email

except ValueError as e:
    # Input validation error → 400 Bad Request
    raise ValueError(f"Input validation failed: {str(e)}")

except RuntimeError as e:
    # Gemini API error → 503 Service Unavailable
    if "API key" in str(e) or "authentication" in str(e):
        raise RuntimeError("Gemini API not configured")
    # Other processing error → 500 Internal Server Error
    raise RuntimeError(f"Email generation failed: {str(e)}")
```

## Testing

### Running Tests

```bash
# Run all email generation tests
pytest test_api_email.py -v

# Run specific test class
pytest test_api_email.py::TestEmailGenerationValidation -v

# Run with coverage
pytest test_api_email.py --cov=backend.agents --cov=backend.api --cov-report=html
```

### Test Categories

1. **Input Validation Tests** (12 tests)
   - Missing fields
   - Invalid values
   - Field length constraints
   - Case sensitivity

2. **Priority Level Tests** (2 tests)
   - All priority levels generate successfully
   - Different priorities produce different tones

3. **Output Format Tests** (4 tests)
   - All required fields present
   - Subject length constraints
   - Email body minimum length
   - Timestamp ISO format

4. **Error Handling Tests** (4 tests)
   - Invalid JSON
   - Unexpected fields
   - Special characters
   - Unicode support

5. **Content Quality Tests** (3 tests)
   - Subject is actual content
   - Email mentions company
   - Professional quality

6. **Integration Tests** (1 test)
   - Multiple sequential requests
   - Different companies produce different results

### Example Test Runs

```bash
# Test validation
pytest test_api_email.py::TestEmailGenerationValidation::test_valid_email_generation_request -v

# Test all priorities
pytest test_api_email.py::TestEmailGenerationPriorities -v

# Test error handling
pytest test_api_email.py::TestEmailGenerationErrors -v
```

## Integration with Other Agents

### Three-Agent Workflow

```
Step 1: Lead Analysis
POST /api/v1/leads/analyze
├── Input: Raw lead data (name, company, role, etc.)
├── Output: LeadAnalysisOutput (8 structured fields)
└── Purpose: Extract and structure lead information

Step 2: Lead Scoring
POST /api/v1/leads/score
├── Input: Lead analysis output
├── Output: LeadScoringOutput (score 0-100, Hot/Warm/Cold, confidence)
└── Purpose: Prioritize leads by purchase intent

Step 3: Email Generation
POST /api/v1/leads/generate-email
├── Input: Lead info + priority from scoring
├── Output: EmailGenerationOutput (subject + email body)
└── Purpose: Create personalized follow-up email
```

### Example Multi-Agent Flow

```python
from backend.agents import (
    lead_analysis_agent,
    lead_scoring_agent,
    email_generator_agent
)

# Raw lead data
raw_lead = {
    "name": "John Doe",
    "title": "VP of Operations",
    "company": "TechCorp",
    "recent_activity": "Downloaded AI implementation guide"
}

# Step 1: Analyze lead
analysis = lead_analysis_agent.analyze_lead(json.dumps(raw_lead))

# Step 2: Score lead
scoring = lead_scoring_agent.score_lead(analysis)

# Step 3: Generate email if Hot or Warm
if scoring.priority in ["Hot", "Warm"]:
    email = email_generator_agent.generate_email(
        company=analysis.company_name,
        requirement=analysis.pain_points,
        budget=analysis.estimated_budget,
        timeline=analysis.decision_timeline,
        priority=scoring.priority
    )
    
    print(f"Send to: {raw_lead['name']} at {raw_lead['company']}")
    print(f"Subject: {email.subject}")
    print(f"Body: {email.email}")
```

## Performance Considerations

### Speed
- **Typical response time**: 2-4 seconds (depends on Gemini API latency)
- **Batch processing**: ~2-4 seconds per email (parallel API calls in future)

### Optimization Strategies
1. **Prompt Caching** - Cache system prompt for repeated generations
2. **Batch API Calls** - Use Gemini batch API for large volumes
3. **Prompt Template Reuse** - Pre-compiled templates for fast generation

### Scalability
- **Concurrent requests**: Limited by Gemini API rate limits
- **Current limit**: ~100 requests/minute (Gemini API default)
- **Recommendation**: Implement request queuing for high volume

## Production Deployment

### Environment Configuration

```bash
# .env file
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
LOG_LEVEL=INFO
DEBUG=False
```

### Monitoring

```python
# Key metrics to monitor
- Email generation success rate
- Average response time
- Error rate by type
- API rate limit usage
- Email quality score feedback
```

### Health Check

```python
# Add this to main.py
@app.get("/health/email-generation")
async def health_email_generation():
    """Check email generation system health."""
    try:
        # Test with sample data
        result = email_generator_agent.generate_email(...)
        return {"status": "healthy", "response_time_ms": 2500}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 503 Service Unavailable | Gemini API not configured | Set GEMINI_API_KEY environment variable |
| 400 Bad Request | Input validation failed | Check field lengths and priority value |
| Empty email body | JSON extraction failed | Add more robust error handling |
| Inconsistent tone | Priority not influencing prompts | Verify priority value is correct |

### Debug Logging

```python
# Enable debug logging in main.py
import logging

logging.basicConfig(level=logging.DEBUG)

# Check logs for:
# - Prompt generation details
# - Gemini API requests/responses
# - JSON extraction attempts
# - Validation errors
```

## Future Enhancements

1. **Industry Customization** - Tone/approach varies by industry
2. **Batch API Integration** - Faster processing for large volumes
3. **A/B Testing** - Generate multiple versions for comparison
4. **Email Template Library** - Pre-built templates for common scenarios
5. **Analytics Dashboard** - Track email open rates, click rates
6. **Multi-language Support** - Generate emails in multiple languages
7. **Dynamic CTA** - Tailor call-to-action based on lead behavior
8. **Integration with Email Services** - Direct send via SendGrid/Mailgun

## Support & Questions

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review [example usage](#usage-examples)
3. Check application logs for detailed error information
4. Contact support with relevant logs and request details

---

**Last Updated**: 2024
**Version**: 1.0
**Status**: Production Ready ✅
