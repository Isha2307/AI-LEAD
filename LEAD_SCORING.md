# Lead Scoring Agent - Complete Implementation Guide

## Overview

The **Lead Scoring Agent** is an AI-powered system that automatically prioritizes sales leads based on comprehensive analysis. It integrates with the Lead Analysis Agent to provide a complete lead qualification workflow.

### Key Features

✓ **AI-Powered Scoring** - Uses Google Gemini API to intelligently score leads
✓ **Prioritization** - Categorizes leads into Hot, Warm, and Cold tiers
✓ **Confidence Metrics** - Provides confidence levels for each assessment
✓ **Detailed Reasoning** - Explains why each score was assigned
✓ **Batch Processing** - Score multiple leads efficiently
✓ **Production-Ready** - Comprehensive error handling and logging

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Routes Layer:                                              │
│  ├─ POST /api/v1/leads/analyze  → LeadAnalysisAgent         │
│  └─ POST /api/v1/leads/score    → LeadScoringAgent          │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Agents Layer:                                              │
│  ├─ LeadAnalysisAgent                                       │
│  │  └─ Analyzes lead information                            │
│  │                                                           │
│  └─ LeadScoringAgent  ← NEW                                 │
│     ├─ Scores analyzed leads                                │
│     ├─ Prioritizes for sales action                         │
│     └─ Provides reasoning                                   │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Services Layer:                                            │
│  └─ GeminiService                                           │
│     ├─ Calls Google Gemini API                              │
│     ├─ Handles JSON extraction                              │
│     └─ Manages error recovery                               │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Prompts Layer:                                             │
│  ├─ Lead Analysis Prompts                                  │
│  └─ Lead Scoring Prompts  ← NEW                            │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Schemas Layer (Pydantic):                                  │
│  ├─ LeadAnalysisRequest/Result                             │
│  ├─ LeadAnalysisOutput                                      │
│  ├─ LeadScoringRequest    ← NEW                            │
│  ├─ LeadScoringResult     ← NEW                            │
│  └─ LeadScoringOutput     ← NEW                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Complete Lead Processing Pipeline

```
LEAD INPUT
    ↓
[LeadAnalysisAgent]
    • Validates lead data
    • Calls Gemini API
    • Extracts structured analysis
    • Returns: name, summary, budget, timeline, urgency, etc.
    ↓
[LeadScoringAgent]  ← NEW
    • Takes analysis results
    • Calls Gemini API for scoring
    • Extracts score (0-100), priority, confidence, reasoning
    • Returns: prioritized lead with recommendations
    ↓
PRIORITIZED LEAD OUTPUT
    • 🔥 Hot: Immediate follow-up needed
    • 🔶 Warm: Investigation recommended
    • ❄️ Cold: Nurture track
```

---

## Scoring System

### Scoring Ranges & Priority Levels

| Score Range | Priority | Symbol | Action | Characteristics |
|-------------|----------|--------|--------|-----------------|
| 80-100 | **Hot** | 🔥 | Immediate follow-up (24 hours) | High fit, urgent need, good budget, near timeline |
| 50-79 | **Warm** | 🔶 | Follow-up within 3-5 days | Medium fit, potential opportunity, needs investigation |
| 0-49 | **Cold** | ❄️ | Add to nurture campaign | Lower priority, poor fit, insufficient information |

### Scoring Factors

The AI considers multiple factors when scoring:

1. **Budget Indicators** (0-25 points)
   - Large budget ranges indicate better fit
   - Enterprise vs SMB vs Startup classification
   - Budget availability and flexibility

2. **Timeline Urgency** (0-25 points)
   - Immediate/ASAP needs score highest
   - Q3/Q4 2024 are near-term
   - Undefined timelines score lower

3. **Urgency Level** (0-25 points)
   - "High" urgency increases score
   - "Medium" scores lower
   - Message tone and clarity

4. **Pain Points** (0-25 points)
   - Multiple pain points indicate better fit
   - Severity and relevance matter
   - Alignment with solution capabilities

### Confidence Scoring

- **80-100% Confidence**: Strong signals, clear indicators
- **60-79% Confidence**: Good signals, some uncertainty
- **40-59% Confidence**: Mixed signals, needs verification
- **0-39% Confidence**: Insufficient information to assess

---

## API Endpoints

### POST /api/v1/leads/score

Score an already-analyzed lead for prioritization.

**Request:**
```json
{
  "name": "John Smith",
  "email": "john@company.com",
  "company": "Company Inc",
  "industry": "Technology",
  "employee_count": 250,
  "lead_message": "We're looking for AI solutions...",
  "analysis": {
    "summary": "Mid-market SaaS company...",
    "requirement": "Lead automation...",
    "budget": "$50K-$100K",
    "timeline": "Q2 2024",
    "urgency": "High",
    "company_size": "Mid-Market",
    "industry": "Software",
    "pain_points": ["Process automation", "Data integration"]
  }
}
```

**Response (200 OK):**
```json
{
  "name": "John Smith",
  "email": "john@company.com",
  "company": "Company Inc",
  "analysis": {
    "summary": "Mid-market SaaS company...",
    "requirement": "Lead automation...",
    "budget": "$50K-$100K",
    "timeline": "Q2 2024",
    "urgency": "High",
    "company_size": "Mid-Market",
    "industry": "Software",
    "pain_points": ["Process automation", "Data integration"]
  },
  "scoring": {
    "lead_score": 87,
    "priority": "Hot",
    "confidence": 92,
    "reasoning": [
      "High urgency indicated in message",
      "Budget range $50K-$100K indicates meaningful investment",
      "Near-term timeline (Q2 2024) shows urgency",
      "Multiple pain points suggest good fit",
      "Mid-market size aligns with solution capabilities"
    ]
  },
  "timestamp": "2024-01-15T10:35:00"
}
```

**Error Responses:**

- **400 Bad Request**: Invalid input data
  ```json
  {
    "detail": "Invalid input: Missing required fields for scoring"
  }
  ```

- **503 Service Unavailable**: Gemini API not configured
  ```json
  {
    "detail": "AI scoring service is not available. Please check Gemini API configuration."
  }
  ```

- **500 Internal Server Error**: Processing error
  ```json
  {
    "detail": "An unexpected error occurred during scoring"
  }
  ```

---

## Implementation Details

### LeadScoringAgent Class

```python
from backend.agents import lead_scoring_agent

# Score a single lead
scoring_result = lead_scoring_agent.score_lead(
    name="John Doe",
    email="john@example.com",
    company="Acme Inc",
    industry="Technology",
    employee_count=500,
    lead_message="We need AI solutions...",
    analysis=analysis_result  # From LeadAnalysisAgent
)

# Score multiple leads
results = lead_scoring_agent.batch_score_leads(
    leads=[
        {
            "name": "Jane Doe",
            "email": "jane@example.com",
            ...
            "analysis": analysis_result_1
        },
        {
            "name": "Bob Smith",
            "email": "bob@example.com",
            ...
            "analysis": analysis_result_2
        }
    ]
)

# Get priority from score
priority = lead_scoring_agent.get_priority_from_score(85)  # Returns "Hot"

# Get action recommendation
recommendation = lead_scoring_agent.get_action_recommendation(scoring_result)
# Returns: "IMMEDIATE FOLLOW-UP: Contact within 24 hours..."
```

### Pydantic Schemas

```python
from backend.schemas import (
    LeadScoringRequest,
    LeadScoringResult,
    LeadScoringOutput
)

# Request validation (automatic)
request: LeadScoringRequest = LeadScoringRequest(...)

# Result validation (automatic)
result: LeadScoringResult = LeadScoringResult(
    lead_score=87,
    priority="Hot",
    confidence=92,
    reasoning=["reason1", "reason2"]
)

# Complete output
output: LeadScoringOutput = LeadScoringOutput(
    name="John Doe",
    email="john@example.com",
    company="Acme Inc",
    analysis=analysis_result,
    scoring=scoring_result,
    timestamp="2024-01-15T10:35:00"
)
```

---

## Complete Workflow Example

### Step 1: Analyze Lead

```bash
curl -X POST http://localhost:8000/api/v1/leads/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@techcorp.com",
    "company": "TechCorp",
    "industry": "Technology",
    "employee_count": 500,
    "lead_message": "We are evaluating AI solutions for our enterprise..."
  }'
```

**Response:**
```json
{
  "name": "Jane Smith",
  "email": "jane@techcorp.com",
  "company": "TechCorp",
  "analysis": {
    "summary": "Enterprise technology company...",
    "requirement": "Enterprise AI platform...",
    "budget": "$200K-$500K",
    "timeline": "Q3 2024",
    "urgency": "High",
    "company_size": "Enterprise",
    "industry": "Technology",
    "pain_points": [...]
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### Step 2: Score Lead

Use the analysis result from Step 1 in the scoring request:

```bash
curl -X POST http://localhost:8000/api/v1/leads/score \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@techcorp.com",
    "company": "TechCorp",
    "industry": "Technology",
    "employee_count": 500,
    "lead_message": "We are evaluating AI solutions for our enterprise...",
    "analysis": {
      "summary": "Enterprise technology company...",
      "requirement": "Enterprise AI platform...",
      "budget": "$200K-$500K",
      "timeline": "Q3 2024",
      "urgency": "High",
      "company_size": "Enterprise",
      "industry": "Technology",
      "pain_points": [...]
    }
  }'
```

**Response:**
```json
{
  "name": "Jane Smith",
  "email": "jane@techcorp.com",
  "company": "TechCorp",
  "analysis": {...},
  "scoring": {
    "lead_score": 94,
    "priority": "Hot",
    "confidence": 95,
    "reasoning": [
      "Enterprise company with large budget ($200K-$500K)",
      "Clear timeline urgency (Q3 2024)",
      "High urgency indicated in message",
      "Multiple critical pain points",
      "Enterprise size indicates significant revenue potential"
    ]
  },
  "timestamp": "2024-01-15T10:35:00"
}
```

### Step 3: Take Action

Based on the score and priority:

- **Hot (87-100)**: Schedule call within 24 hours
- **Warm (50-86)**: Email with value message within 3-5 days
- **Cold (0-49)**: Add to nurture sequence

---

## Usage Examples

### Single Lead Scoring

```python
from backend.agents import lead_analyzer_agent, lead_scoring_agent

# Analyze lead
analysis = lead_analyzer_agent.analyze_lead(
    name="John Smith",
    email="john@company.com",
    company="Company Inc",
    industry="Technology",
    employee_count=250,
    lead_message="We need help with AI implementation..."
)

# Score lead
scoring = lead_scoring_agent.score_lead(
    name="John Smith",
    email="john@company.com",
    company="Company Inc",
    industry="Technology",
    employee_count=250,
    lead_message="We need help with AI implementation...",
    analysis=analysis
)

# Use the results
print(f"Score: {scoring.lead_score}/100")
print(f"Priority: {scoring.priority}")
print(f"Confidence: {scoring.confidence}%")
print(f"Reasoning: {', '.join(scoring.reasoning)}")
```

### Batch Lead Scoring

```python
leads_with_analysis = [
    {
        "name": "John Doe",
        "email": "john@example1.com",
        "company": "Company 1",
        "industry": "Tech",
        "employee_count": 100,
        "lead_message": "...",
        "analysis": analysis_1
    },
    {
        "name": "Jane Smith",
        "email": "jane@example2.com",
        "company": "Company 2",
        "industry": "Finance",
        "employee_count": 500,
        "lead_message": "...",
        "analysis": analysis_2
    }
]

results = lead_scoring_agent.batch_score_leads(leads_with_analysis)

# Process results
for result in results:
    if result["status"] == "success":
        print(f"{result['lead']['company']}: {result['scoring']['lead_score']}/100")
    else:
        print(f"Failed to score {result['lead']['company']}: {result['error']}")
```

---

## Error Handling

### Common Errors and Solutions

**Error: "Gemini service is not available"**
- **Cause**: GEMINI_API_KEY not configured
- **Solution**: Add GEMINI_API_KEY to `.env` file

**Error: "Invalid input validation error"**
- **Cause**: Missing required fields in request
- **Solution**: Verify all required fields are present and valid

**Error: "Invalid response format from AI service"**
- **Cause**: Gemini returned malformed JSON
- **Solution**: Check Gemini API logs, retry with same lead data

**Error: "AI service temporarily unavailable"**
- **Cause**: Gemini API is down or rate-limited
- **Solution**: Retry after a few seconds, check API status

---

## Performance Considerations

### Benchmarks

- **Single Lead Scoring**: ~2-3 seconds (includes Gemini API call)
- **Batch Processing** (10 leads): ~20-30 seconds
- **Concurrent Requests**: Handled by FastAPI async processing

### Optimization Tips

1. **Batch Processing**: Score multiple leads in single operation
2. **Caching**: Cache analysis results if scoring multiple times
3. **Async**: Use FastAPI's async capabilities for concurrent requests
4. **Rate Limiting**: Implement rate limiting to avoid API throttling

---

## Production Deployment Checklist

### Pre-Deployment

- [ ] Configure GEMINI_API_KEY in environment
- [ ] Verify Gemini API access and quotas
- [ ] Test with sample leads
- [ ] Run VERIFY.py for component checks
- [ ] Review scoring ranges for your domain
- [ ] Configure logging appropriately

### Deployment

- [ ] Set up error monitoring (e.g., Sentry)
- [ ] Configure log aggregation
- [ ] Set up database backups
- [ ] Enable HTTPS
- [ ] Configure CORS as needed
- [ ] Set up API rate limiting

### Post-Deployment

- [ ] Monitor API response times
- [ ] Track scoring accuracy
- [ ] Review error logs regularly
- [ ] Gather feedback from sales team
- [ ] Iterate on scoring factors based on feedback
- [ ] Update prompts based on results

---

## Customization

### Adjusting Scoring Factors

Edit the Gemini prompt in `backend/prompts/lead_prompts.py`:

```python
def get_lead_scoring_prompt(lead_data: dict, analysis_data: dict) -> str:
    # Modify the scoring guidelines here
    prompt = f"""
    ...
    SCORING GUIDELINES:
    - 80-100: Hot (Adjust criteria here)
    - 50-79: Warm (Adjust criteria here)
    - 0-49: Cold (Adjust criteria here)
    ...
    """
```

### Changing Priority Levels

Modify priority mapping in `backend/agents/lead_scorer.py`:

```python
def get_priority_from_score(self, score: int) -> str:
    if score >= 80:  # Adjust threshold
        return "Hot"
    elif score >= 50:  # Adjust threshold
        return "Warm"
    else:
        return "Cold"
```

---

## Testing

### Test the Endpoint

```bash
# Run example
python example_lead_scoring.py

# Test API
python test_api.py

# Verify components
python VERIFY.py
```

### Unit Tests

```python
from backend.agents.lead_scorer import LeadScoringAgent
from backend.schemas import LeadAnalysisResult

# Create agent
agent = LeadScoringAgent()

# Create mock analysis
analysis = LeadAnalysisResult(
    summary="Test summary",
    requirement="Test requirement",
    budget="$100K",
    timeline="Q2 2024",
    urgency="High",
    company_size="Mid-Market",
    industry="Technology",
    pain_points=["Pain point 1", "Pain point 2"]
)

# Score lead
result = agent.score_lead(
    name="Test Lead",
    email="test@example.com",
    company="Test Company",
    industry="Technology",
    employee_count=100,
    lead_message="Test message",
    analysis=analysis
)

# Verify result
assert 0 <= result.lead_score <= 100
assert result.priority in ["Hot", "Warm", "Cold"]
assert 0 <= result.confidence <= 100
assert len(result.reasoning) > 0
```

---

## Support & Troubleshooting

### Getting Help

1. Check `VERIFY.py` output for configuration issues
2. Review logs in backend/logs (if available)
3. Test with `example_lead_scoring.py`
4. Check GEMINI_API_KEY configuration
5. Review error messages in HTTP responses

### Common Issues

**Q: Scoring takes too long**
A: This is normal (2-3 seconds for Gemini API call). Optimize with batch processing.

**Q: Scores vary between runs**
A: Expected - Gemini makes judgment calls. Confidence field indicates variability.

**Q: Always getting same priority**
A: Leads may genuinely have similar fit. Review example leads for diversity.

---

## Summary

The Lead Scoring Agent provides:

✓ **Intelligent Prioritization** - AI-powered lead scoring 0-100
✓ **Clear Priority Levels** - Hot/Warm/Cold for quick triage
✓ **Confidence Metrics** - Know how reliable each score is
✓ **Detailed Reasoning** - Understand why leads are prioritized
✓ **Production Ready** - Comprehensive error handling and logging
✓ **Easy Integration** - Simple Python API and HTTP endpoints

For more information, see:
- [LEAD_ANALYSIS.md](LEAD_ANALYSIS.md) - Lead Analysis Agent details
- [QUICK_START.py](QUICK_START.py) - Setup instructions
- [example_lead_scoring.py](example_lead_scoring.py) - Complete examples
