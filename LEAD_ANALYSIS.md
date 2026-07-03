# Lead Analysis Agent - Implementation Guide

## Overview

The Lead Analysis Agent is a production-grade AI-powered system that analyzes sales leads using Google's Gemini API. It extracts structured insights, validates responses using Pydantic, and provides comprehensive error handling.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API Endpoint                              │
│              POST /api/v1/leads/analyze                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            LeadAnalysisRequest (Pydantic)                    │
│  - name, email, company, industry                            │
│  - employee_count, lead_message                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          LeadAnalysisAgent.analyze_lead()                    │
│  1. Input validation                                         │
│  2. Prompt generation                                        │
│  3. Gemini API call                                          │
│  4. Response parsing                                         │
│  5. Schema validation                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           GeminiService.analyze_lead()                       │
│  - Calls Google Generative AI API                            │
│  - Extracts JSON from response                               │
│  - Handles errors gracefully                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         LeadAnalysisResult (Pydantic Schema)                 │
│  {                                                           │
│    "summary": "...",                                         │
│    "requirement": "...",                                     │
│    "budget": "...",                                          │
│    "timeline": "...",                                        │
│    "urgency": "...",                                         │
│    "company_size": "...",                                    │
│    "industry": "...",                                        │
│    "pain_points": [...]                                      │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. LeadAnalysisAgent (`backend/agents/lead_analyzer.py`)

**Purpose**: Orchestrates the lead analysis workflow

**Key Methods**:

- `analyze_lead()`: Main analysis method
  - Validates input parameters
  - Generates analysis prompts
  - Calls Gemini API
  - Parses and validates responses
  - Calculates qualification scores

- `batch_analyze_leads()`: Analyzes multiple leads
  - Processes leads sequentially
  - Handles individual failures gracefully
  - Returns summary with success/failure counts

- `get_qualification_score()`: Scoring logic
  - Analyzes budget, timeline, urgency
  - Counts pain points
  - Returns score (0-100) and qualification status

**Example Usage**:
```python
from backend.agents import lead_analyzer_agent

# Analyze a single lead
analysis = lead_analyzer_agent.analyze_lead(
    name="John Smith",
    email="john@company.com",
    company="Tech Corp",
    industry="Software",
    employee_count=500,
    lead_message="We need AI-powered lead qualification"
)

# Get qualification score
score, is_qualified = lead_analyzer_agent.get_qualification_score(analysis)
```

### 2. GeminiService (`backend/services/gemini_service.py`)

**Purpose**: Handles all Gemini API interactions

**Key Methods**:

- `_initialize_client()`: Sets up Gemini connection
- `analyze_lead()`: Calls Gemini API for analysis
- `generate_followup()`: Generates follow-up messages
- `extract_json_from_text()`: Robust JSON extraction

**Features**:
- Retries on API errors
- Handles Gemini response formats (JSON, markdown, wrapped)
- Comprehensive logging
- Singleton pattern for resource efficiency

### 3. Pydantic Schemas

#### LeadAnalysisRequest
```python
{
    "name": str,
    "email": str (EmailStr),
    "company": str,
    "industry": str,
    "employee_count": int,
    "lead_message": str
}
```

#### LeadAnalysisResult
```python
{
    "summary": str,
    "requirement": str,
    "budget": str,
    "timeline": str,
    "urgency": str,
    "company_size": str,
    "industry": str,
    "pain_points": list[str]
}
```

### 4. Prompt Engineering

Located in `backend/prompts/lead_prompts.py`:

**Analysis Prompt**:
- Instructs Gemini to analyze lead as B2B sales analyst
- Returns ONLY valid JSON
- Specifies exact field names and formats
- Includes context about the lead

**System Prompts**:
- `SYSTEM_PROMPT_LEAD_ANALYST`: Expert analyst persona
- `SYSTEM_PROMPT_FOLLOW_UP`: Sales copywriter persona

## API Endpoint

### POST /api/v1/leads/analyze

**Request**:
```json
{
  "name": "John Smith",
  "email": "john.smith@company.com",
  "company": "Tech Solutions Inc",
  "industry": "Software/SaaS",
  "employee_count": 250,
  "lead_message": "We're looking for AI-powered lead qualification..."
}
```

**Success Response (200)**:
```json
{
  "name": "John Smith",
  "email": "john.smith@company.com",
  "company": "Tech Solutions Inc",
  "analysis": {
    "summary": "Enterprise SaaS company seeking AI automation...",
    "requirement": "Automated lead scoring and qualification",
    "budget": "$50K-$100K",
    "timeline": "Q3 2024",
    "urgency": "High",
    "company_size": "Mid-Market",
    "industry": "Software",
    "pain_points": [
      "Manual lead review is time-consuming",
      "Inconsistent qualification criteria",
      "Sales team lacks visibility into lead quality"
    ]
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

**Error Response (400)**:
```json
{
  "detail": "Invalid input: Missing required fields"
}
```

**Error Response (503)**:
```json
{
  "detail": "AI service temporarily unavailable. Please try again."
}
```

## Error Handling

The system implements comprehensive error handling:

### Input Validation Errors (400)
- Missing required fields
- Invalid email format
- Invalid employee count

### API Errors (503)
- Gemini API unavailable
- Quota exceeded
- Network errors

### Parse/Validation Errors (500)
- Invalid JSON from Gemini
- Schema validation failures
- Unexpected response format

## Qualification Scoring Logic

The `get_qualification_score()` method implements business logic:

```
Base Score: 0

+ 25 points: Enterprise budget or $100K+
+ 15 points: Mid-market budget ($10K-$100K)

+ 25 points: Immediate or near-term timeline
+ 15 points: Mid-term timeline (3-6 months)

+ 25 points: High urgency
+ 15 points: Medium urgency

+ 20 points: 3+ identified pain points
+ 10 points: 1-2 identified pain points

Qualification Threshold: Score >= 60
```

Customize this logic in `lead_analyzer_agent.get_qualification_score()`.

## Environment Setup

### Required Environment Variables

```env
# Gemini API
GEMINI_API_KEY=sk-proj-xxxxx

# Optional (defaults provided)
GEMINI_MODEL=gemini-pro
DEBUG=False
LOG_LEVEL=INFO
```

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or specifically for Gemini
pip install google-generativeai==0.5.0
```

## Usage Examples

### 1. Direct Agent Usage

```python
from backend.agents import lead_analyzer_agent

# Analyze a lead
try:
    result = lead_analyzer_agent.analyze_lead(
        name="Alice Johnson",
        email="alice@startup.io",
        company="StartupIO",
        industry="Fintech",
        employee_count=50,
        lead_message="Looking to implement AI sales tools"
    )
    
    print(f"Summary: {result.summary}")
    print(f"Pain Points: {result.pain_points}")
    
    # Get score
    score, qualified = lead_analyzer_agent.get_qualification_score(result)
    print(f"Score: {score}/100, Qualified: {qualified}")
    
except ValueError as e:
    print(f"Validation error: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

### 2. API Request (cURL)

```bash
curl -X POST "http://localhost:8000/api/v1/leads/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Michael Chen",
    "email": "michael@enterprise.com",
    "company": "Enterprise Global",
    "industry": "Manufacturing",
    "employee_count": 5000,
    "lead_message": "Need enterprise lead management platform for 50+ sales reps"
  }'
```

### 3. Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/leads/analyze",
    json={
        "name": "Sarah Wilson",
        "email": "sarah@company.com",
        "company": "Global Solutions",
        "industry": "Consulting",
        "employee_count": 1000,
        "lead_message": "Exploring AI solutions for sales automation"
    }
)

if response.status_code == 200:
    analysis = response.json()
    print(analysis["analysis"]["pain_points"])
```

## Testing

### Run Example Script

```bash
# Demonstrates single and batch analysis
python example_lead_analysis.py
```

### Test API Endpoint

```bash
# Run API tests
python test_api.py
```

### Manual Testing

```bash
# Terminal 1: Start backend
python -m backend.main

# Terminal 2: Run tests
python test_api.py
```

## Logging

The system includes comprehensive logging:

**Log Levels**:
- INFO: Analysis start/completion
- DEBUG: Response parsing, prompt generation
- ERROR: API failures, validation errors
- WARNING: API key missing, graceful degradation

**View Logs**:
```python
from backend.utils import app_logger

app_logger.info("Custom log message")
```

## Performance Considerations

1. **API Latency**: Gemini API typically responds in 2-5 seconds
2. **Singleton Pattern**: GeminiService initialized once, reused
3. **Batch Processing**: Sequential processing recommended (rate limits)
4. **Caching**: Consider caching similar leads for cost optimization

## Customization

### Custom Scoring Logic

Edit `lead_analyzer_agent.get_qualification_score()`:

```python
def get_qualification_score(self, analysis: LeadAnalysisResult) -> tuple[float, bool]:
    score = 0.0
    
    # Add your custom scoring logic
    if "Enterprise" in analysis.company_size:
        score += 50
    
    # etc.
    
    is_qualified = score >= 60
    return score, is_qualified
```

### Custom Prompts

Edit `backend/prompts/lead_prompts.py`:

```python
def get_lead_analysis_prompt(lead_data: dict) -> str:
    # Customize the analysis prompt
    prompt = f"""
    Your custom prompt here...
    """
    return prompt
```

### Custom Analysis Fields

Update `LeadAnalysisResult` in `backend/schemas/lead_schema.py`:

```python
class LeadAnalysisResult(BaseModel):
    summary: str
    new_custom_field: str  # Add here
    # etc.
```

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"

```bash
# Solution: Add to .env
GEMINI_API_KEY=your_actual_key_here
```

### Issue: "Invalid JSON from Gemini"

The system attempts multiple JSON extraction methods:
1. Direct JSON parsing
2. Markdown code block extraction
3. JSON object detection

If still failing, Gemini may be returning non-JSON. Check:
- Prompt clarity in `lead_prompts.py`
- API response in debug logs

### Issue: Analysis taking too long

- Check network connection
- Verify API quota in Google Cloud Console
- Consider batch size optimization

## Production Checklist

- [ ] GEMINI_API_KEY configured in production env
- [ ] Error monitoring set up
- [ ] Rate limiting configured
- [ ] Logging aggregation enabled
- [ ] API authentication implemented
- [ ] Response caching considered
- [ ] Load testing completed
- [ ] Cost monitoring active

## Next Steps

1. **Test Thoroughly**: Use example_lead_analysis.py and test_api.py
2. **Fine-tune Prompts**: Customize for your lead profile
3. **Adjust Scoring**: Implement your qualification logic
4. **Add Auth**: Implement API authentication
5. **Monitor**: Set up logging and error tracking
6. **Deploy**: Move to production environment

## References

- [Google Generative AI Docs](https://cloud.google.com/docs/generative-ai/latest)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Project README](README.md)
