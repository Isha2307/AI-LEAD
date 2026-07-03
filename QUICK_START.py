"""
Quick Start Guide for Lead Analysis Agent

This file provides step-by-step instructions to:
1. Set up the environment
2. Configure Gemini API
3. Test the lead analysis feature
4. Integrate with your application
"""

# ========================================
# QUICK START SETUP (5 minutes)
# ========================================

# Step 1: Get Gemini API Key
# --------------------------
# 1. Go to https://makersuite.google.com/app/apikey
# 2. Click "Create API Key" or use existing key
# 3. Copy the API key


# Step 2: Configure Environment
# ---------
# Create .env file in project root:

"""
GEMINI_API_KEY=sk-proj-your_actual_key_here
DATABASE_URL=sqlite:///./ai_lead.db
DEBUG=False
LOG_LEVEL=INFO
"""

# Step 3: Install Dependencies
# Run in terminal:
"""
pip install -r requirements.txt
"""

# Step 4: Start Backend
# Run in terminal:
"""
python -m backend.main
"""
# Expected output:
# - INFO:     Uvicorn running on http://0.0.0.0:8000
# - INFO:     LeadAnalysisAgent initialized successfully


# ========================================
# TESTING (2 minutes)
# ========================================

# Option A: Run Example Script
"""
python example_lead_analysis.py
"""
# Shows complete analysis with all fields

# Option B: Test API Endpoint
"""
python test_api.py
"""
# Test with example curl and Python requests


# Option C: Manual cURL Test
"""
curl -X POST "http://localhost:8000/api/v1/leads/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "email": "john@example.com",
    "company": "Example Corp",
    "industry": "Technology",
    "employee_count": 100,
    "lead_message": "We need AI-powered lead qualification for our sales team."
  }' | python -m json.tool
"""


# ========================================
# BASIC USAGE
# ========================================

# PROGRAMMATIC USAGE

# 1. Django/Flask Backend Integration
from backend.agents import lead_analyzer_agent

def qualify_lead(lead_data):
    try:
        analysis = lead_analyzer_agent.analyze_lead(
            name=lead_data['name'],
            email=lead_data['email'],
            company=lead_data['company'],
            industry=lead_data['industry'],
            employee_count=lead_data['employee_count'],
            lead_message=lead_data['message']
        )
        
        score, is_qualified = lead_analyzer_agent.get_qualification_score(analysis)
        
        return {
            'analysis': analysis.model_dump(),
            'score': score,
            'qualified': is_qualified
        }
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None


# 2. API Endpoint (Already Implemented)
# POST http://localhost:8000/api/v1/leads/analyze

# Request:
request_payload = {
    "name": "Jane Doe",
    "email": "jane@company.com",
    "company": "Company Inc",
    "industry": "Finance",
    "employee_count": 500,
    "lead_message": "Looking for sales automation solutions with AI"
}

# Response:
response_example = {
    "name": "Jane Doe",
    "email": "jane@company.com",
    "company": "Company Inc",
    "analysis": {
        "summary": "Finance sector, mid-market company seeking sales automation...",
        "requirement": "Automated lead scoring and sales process optimization",
        "budget": "$50K-$150K",
        "timeline": "Q2 2024",
        "urgency": "High",
        "company_size": "Mid-Market",
        "industry": "Finance",
        "pain_points": [
            "Manual lead review consuming 40+ hours/week",
            "Inconsistent qualification across sales team",
            "Lost opportunities due to slow response times"
        ]
    },
    "timestamp": "2024-01-15T10:30:00"
}


# ========================================
# RESPONSE PARSING
# ========================================

import json

# Parse analysis result
analysis = response_example['analysis']

# Access fields
print(f"Summary: {analysis['summary']}")
print(f"Budget: {analysis['budget']}")
print(f"Timeline: {analysis['timeline']}")
print(f"Urgency: {analysis['urgency']}")

# Work with pain points
for i, pain_point in enumerate(analysis['pain_points'], 1):
    print(f"{i}. {pain_point}")

# Create follow-up actions based on analysis
if analysis['urgency'] == 'High':
    print("✓ Priority follow-up needed")

if 'Sales automation' in analysis['requirement']:
    print("✓ Product fit verified")


# ========================================
# ERROR HANDLING
# ========================================

import requests

try:
    response = requests.post(
        "http://localhost:8000/api/v1/leads/analyze",
        json=request_payload,
        timeout=30
    )
    
    if response.status_code == 200:
        analysis = response.json()
        # Process successful response
        
    elif response.status_code == 400:
        # Validation error
        error = response.json()
        print(f"Invalid input: {error['detail']}")
        
    elif response.status_code == 503:
        # Service unavailable
        error = response.json()
        print(f"AI service unavailable: {error['detail']}")
        
    else:
        # Other error
        print(f"Unexpected error: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("Cannot connect to API. Make sure backend is running.")
except requests.exceptions.Timeout:
    print("Request timeout. API may be experiencing issues.")


# ========================================
# BATCH ANALYSIS
# ========================================

# Analyze multiple leads
leads = [
    {
        "name": "John Smith",
        "email": "john@company1.com",
        "company": "Company 1",
        "industry": "Tech",
        "employee_count": 100,
        "lead_message": "Interested in lead qualification tools"
    },
    {
        "name": "Jane Doe",
        "email": "jane@company2.com",
        "company": "Company 2",
        "industry": "Finance",
        "employee_count": 500,
        "lead_message": "Need sales automation for 50+ team"
    }
]

# Process batch
if lead_analyzer_agent:
    results = lead_analyzer_agent.batch_analyze_leads(leads)
    
    for result in results:
        if result['status'] == 'success':
            analysis = result['analysis']
            print(f"✓ {result['lead']['name']}: {analysis['summary'][:50]}...")
        else:
            print(f"✗ {result['lead']['name']}: {result['error']}")


# ========================================
# COMMON ISSUES & SOLUTIONS
# ========================================

# Issue 1: "GEMINI_API_KEY not configured"
# Solution: Add GEMINI_API_KEY to .env file

# Issue 2: "Cannot connect to API"
# Solution: Start backend with: python -m backend.main

# Issue 3: "Invalid JSON from Gemini"
# Solution: Check lead data is valid and complete

# Issue 4: Long response times (>10 seconds)
# Solution: 
# - Check internet connection
# - Verify API quota
# - Try simpler lead message

# Issue 5: 503 Service Unavailable
# Solution:
# - Check Gemini API quota/limits
# - Check Google Cloud credentials
# - Verify network connection


# ========================================
# CUSTOMIZATION
# ========================================

# 1. ADJUST SCORING LOGIC
# Edit: backend/agents/lead_analyzer.py
# Method: get_qualification_score()

# 2. MODIFY PROMPTS
# Edit: backend/prompts/lead_prompts.py
# Customize analysis prompt for your needs

# 3. ADD FIELDS TO ANALYSIS
# Edit: backend/schemas/lead_schema.py
# Add fields to LeadAnalysisResult

# 4. CHANGE QUALIFICATION THRESHOLD
# Edit: lead_analyzer.py, line ~290
# Modify: is_qualified = score >= 60


# ========================================
# NEXT STEPS
# ========================================

# 1. Test the API: python test_api.py
# 2. Review analysis results
# 3. Customize prompts for your domain
# 4. Adjust scoring logic
# 5. Integrate with your CRM
# 6. Set up production deployment
# 7. Monitor API usage and costs


# ========================================
# RESOURCES
# ========================================

# Complete Documentation: LEAD_ANALYSIS.md
# API Testing: test_api.py
# Examples: example_lead_analysis.py
# API Docs: http://localhost:8000/api/docs
# README: README.md


print("""
╔════════════════════════════════════════════════════════════════╗
║         LEAD ANALYSIS AGENT - QUICK START COMPLETE             ║
╚════════════════════════════════════════════════════════════════╝

✓ Setup guide ready
✓ Testing examples provided
✓ API documentation available
✓ Customization options documented

Next Steps:
1. Configure .env with GEMINI_API_KEY
2. Run: python -m backend.main
3. Test: python test_api.py
4. Review: LEAD_ANALYSIS.md for full documentation

Happy analyzing! 🚀
""")
