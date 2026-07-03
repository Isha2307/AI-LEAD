# Email Generation Agent - Quick Start Guide

## 5-Minute Setup

### 1. Verify Installation ✅

```bash
# Check that required packages are installed
pip list | grep -E "fastapi|google-generativeai|pydantic"

# Expected output:
# fastapi                0.104.1
# google-generativeai    0.5.0
# pydantic              2.5.2
```

### 2. Configure Environment 🔑

```bash
# Set your Gemini API key (from Google Cloud Console)
export GEMINI_API_KEY="your_api_key_here"

# Or create .env file in project root:
GEMINI_API_KEY=your_api_key_here
DEBUG=False
LOG_LEVEL=INFO
```

### 3. Start the Server 🚀

```bash
# From project root directory
cd c:\Users\Isha\OneDrive\Documents\AI_LEAD

# Start the FastAPI server
python -m uvicorn backend.main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

### 4. Test the API 🧪

```bash
# In another terminal, test with a simple curl command
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "TechCorp Solutions",
    "requirement": "Enterprise AI platform for customer support",
    "budget": "$200K-$500K",
    "timeline": "Q2 2024 (immediate)",
    "priority": "Hot"
  }'

# Expected response (200 OK):
# {
#   "company": "TechCorp Solutions",
#   "requirement": "Enterprise AI platform for customer support",
#   "priority": "Hot",
#   "email_content": {
#     "subject": "Let's Accelerate Your Customer Support Transformation",
#     "email": "John,\n\nI noticed [...]"
#   },
#   "timestamp": "2024-01-15T10:30:00Z"
# }
```

## Common Use Cases

### Generate a Hot Lead Email (Urgency)

```bash
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Enterprise Corp",
    "requirement": "Full AI strategy for digital transformation",
    "budget": "$500K+",
    "timeline": "Q2 2024 (immediate)",
    "priority": "Hot"
  }'
```

**Characteristics:**
- Urgent tone
- Strong call-to-action
- Focus on immediate value
- Quick next step

### Generate a Warm Lead Email (Nurturing)

```bash
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "MidMarket Services",
    "requirement": "Process automation for back-office operations",
    "budget": "$100K-$150K",
    "timeline": "Q3 2024 (3 months away)",
    "priority": "Warm"
  }'
```

**Characteristics:**
- Consultative tone
- Educational focus
- Build interest gradually
- Gentle next step

### Generate a Cold Lead Email (Value-First)

```bash
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "StartupXYZ",
    "requirement": "Exploratory AI tools for product development",
    "budget": "$20K-$30K (uncertain)",
    "timeline": "Unknown",
    "priority": "Cold"
  }'
```

**Characteristics:**
- Helpful tone
- Value-focused
- No pressure
- Soft next step

## Python Examples

### Single Email Generation

```python
from backend.agents import email_generator_agent

# Generate one email
result = email_generator_agent.generate_email(
    company="TechCorp Solutions",
    requirement="Enterprise AI platform for customer support",
    budget="$200K-$500K",
    timeline="Q2 2024",
    priority="Hot"
)

print(f"Subject: {result.subject}")
print(f"Email:\n{result.email}")
```

### Batch Email Generation

```python
from backend.agents import email_generator_agent

leads = [
    {
        "company": "CompanyA",
        "requirement": "AI for customer support",
        "budget": "$500K+",
        "timeline": "Q2 2024",
        "priority": "Hot"
    },
    {
        "company": "CompanyB",
        "requirement": "Process automation",
        "budget": "$100K-$150K",
        "timeline": "Q3 2024",
        "priority": "Warm"
    },
    {
        "company": "CompanyC",
        "requirement": "Data analytics",
        "budget": "$50K",
        "timeline": "Unknown",
        "priority": "Cold"
    },
]

results = email_generator_agent.batch_generate_emails(leads)

for lead, email in zip(leads, results):
    print(f"\n{lead['company']} ({lead['priority']}):")
    print(f"  Subject: {email.subject}")
```

### API Client (Python)

```python
import requests

url = "http://localhost:8000/api/v1/leads/generate-email"

payload = {
    "company": "TechCorp",
    "requirement": "Enterprise AI platform",
    "budget": "$200K-$500K",
    "timeline": "Q2 2024",
    "priority": "Hot"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Subject: {data['email_content']['subject']}")
    print(f"Email: {data['email_content']['email']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

## Understanding Priorities

### 🔥 Hot (Score 80-100)

**When to use:**
- Prospect has strong buying signals
- Budget is approved/available
- Timeline is immediate (Q1, Q2)
- Decision makers engaged

**Email tone:**
- Urgent and enthusiastic
- Express understanding of timeline
- Immediate next step (meeting this week)
- Focus on quick implementation

**Example subject:**
> "Let's Talk About Your Q2 Transformation Timeline"

### 🔶 Warm (Score 50-79)

**When to use:**
- Prospect shows genuine interest
- Budget is likely but not approved
- Timeline is medium-term (Q2, Q3)
- Initial qualification underway

**Email tone:**
- Professional and consultative  
- Share relevant case study/insight
- Next step for following week
- Focus on building confidence

**Example subject:**
> "How Companies Like Yours Are Approaching AI Implementation"

### ❄️ Cold (Score 0-49)

**When to use:**
- Early exploration stage
- Budget uncertain/not approved
- Timeline undefined or distant
- Initial awareness only

**Email tone:**
- Helpful and value-focused
- Lead with insight, not need
- Soft CTA (no pressure)
- Focus on long-term relationship

**Example subject:**
> "AI Trends Reshaping Your Industry [Research]"

## Troubleshooting

### "503 Service Unavailable"

**Problem:** Gemini API not configured

**Solution:**
```bash
# Check environment variable
echo $GEMINI_API_KEY

# If empty, set it:
export GEMINI_API_KEY="your_key_here"

# Or add to .env file in project root
```

### "400 Bad Request"

**Problem:** Input validation failed

**Cause:** Check these constraints:
- `company`: 1-255 characters
- `requirement`: 10+ characters
- `budget`: 1-100 characters
- `timeline`: 1-100 characters
- `priority`: Must be "Hot", "Warm", or "Cold" (case-sensitive)

**Solution:**
```bash
# Example of INVALID request
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -d '{
    "company": "",               # ❌ Empty
    "requirement": "AI",         # ❌ Too short
    "budget": "$200K",
    "timeline": "Q2",
    "priority": "hot"            # ❌ Wrong case
  }'

# Example of VALID request
curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
  -d '{
    "company": "TechCorp",       # ✅ 1-255 chars
    "requirement": "AI platform", # ✅ 10+ chars
    "budget": "$200K",
    "timeline": "Q2 2024",
    "priority": "Hot"            # ✅ Correct case
  }'
```

### No API Key Found

**Problem:** "GEMINI_API_KEY not found"

**Solution:**
```bash
# Get API key at https://makersuite.google.com/app/apikey

# Method 1: Environment variable
export GEMINI_API_KEY="your_key_here"

# Method 2: .env file
echo "GEMINI_API_KEY=your_key_here" > .env

# Method 3: Update backend/config.py
GEMINI_API_KEY = "your_key_here"  # Not recommended for production
```

## File Structure Reference

```
backend/
├── agents/
│   ├── email_generator.py      # EmailGenerationAgent class
│   └── __init__.py
├── schemas/
│   ├── lead_schema.py          # Email schemas
│   └── __init__.py
├── prompts/
│   ├── lead_prompts.py         # Email prompts
│   └── __init__.py
├── services/
│   └── gemini_service.py       # Gemini API client
├── api/
│   └── routes/
│       └── leads.py            # FastAPI endpoints
└── main.py                     # FastAPI app
```

## Running Examples

```bash
# Example 1: Email generation demonstration
python example_email_generation.py

# Example 2: Integrated workflow (all 3 agents)
python example_integrated_workflow.py

# Example 3: Run tests
pytest test_api_email.py -v
```

## Next Steps

### For Integration
1. Add email generation to your application
2. Connect to your CRM/database
3. Schedule batch email processing
4. Monitor email metrics

### For Customization
1. Modify system prompts in `backend/prompts/lead_prompts.py`
2. Adjust email tone/length parameters
3. Add industry-specific customization
4. Implement A/B testing

### For Production
1. Add authentication to API endpoints
2. Implement rate limiting
3. Add email service integration (SendGrid, etc.)
4. Monitor Gemini API usage
5. Set up error alerts

## API Reference Quick Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/leads/generate-email` | POST | Generate personalized email |

**Request:**
```json
{
  "company": "string (1-255)",
  "requirement": "string (10+)",
  "budget": "string (1-100)",
  "timeline": "string (1-100)",
  "priority": "Hot|Warm|Cold"
}
```

**Response (200):**
```json
{
  "company": "string",
  "requirement": "string",
  "priority": "string",
  "email_content": {
    "subject": "string",
    "email": "string"
  },
  "timestamp": "ISO-8601 datetime"
}
```

## Support Resources

- **Full Documentation:** See [EMAIL_GENERATION.md](EMAIL_GENERATION.md)
- **Code Examples:** See `example_*.py` files
- **API Tests:** See [test_api_email.py](test_api_email.py)
- **Integration Guide:** See [example_integrated_workflow.py](example_integrated_workflow.py)

## Best Practices

✅ **Do:**
- Use appropriate priority levels based on lead score
- Include specific company names
- Provide realistic budget/timeline ranges
- Monitor email generation metrics

❌ **Don't:**
- Use generic company names like "Company ABC"
- Provide unrealistic budgets
- Use incorrect priority values
- Call the API more frequently than necessary

---

Ready to generate professional emails? Start with the 5-minute setup above! 🚀
