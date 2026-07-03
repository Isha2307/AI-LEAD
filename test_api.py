"""
API Testing Script for Lead Analysis Endpoint.

This script provides examples of:
1. How to call the analyze endpoint
2. Expected request/response formats
3. Error handling scenarios
4. Using with curl commands
5. Using with Python requests library

To test the API:
1. Start backend: python -m backend.main
2. Run this script or use curl commands below
"""

import json
import requests
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
ANALYZE_ENDPOINT = f"{BASE_URL}/leads/analyze"


def test_lead_analysis(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test the lead analysis endpoint.
    
    Args:
        lead_data: Dictionary with lead information
    
    Returns:
        API response
    """
    print(f"\n📤 Sending request to: {ANALYZE_ENDPOINT}")
    print(f"📋 Payload: {json.dumps(lead_data, indent=2)}")
    
    try:
        response = requests.post(
            ANALYZE_ENDPOINT,
            json=lead_data,
            timeout=30,
        )
        
        print(f"\n📨 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS - Analysis Results:")
            print(json.dumps(result, indent=2))
            return result
        else:
            print(f"\n❌ ERROR:")
            print(json.dumps(response.json(), indent=2))
            return None
            
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR: Cannot connect to API")
        print("   Make sure the backend is running: python -m backend.main")
        return None
    
    except requests.exceptions.Timeout:
        print("\n❌ TIMEOUT: Request took too long")
        return None
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return None


def main():
    """Run API tests."""
    print("="*80)
    print("🤖 LEAD ANALYSIS API - TESTING SCRIPT")
    print("="*80)
    
    # Test 1: Valid lead analysis
    print("\n🧪 TEST 1: Valid Lead Analysis")
    print("-"*80)
    
    valid_lead = {
        "name": "Sarah Thompson",
        "email": "sarah.thompson@corporation.com",
        "company": "Global Corporation Inc",
        "industry": "Financial Services",
        "employee_count": 1500,
        "lead_message": "We need to modernize our sales operations with AI-powered lead scoring. "
                       "Currently using spreadsheets and manual reviews. Budget approved for Q4. "
                       "Need implementation within 60 days.",
    }
    
    test_lead_analysis(valid_lead)
    
    # Test 2: Another valid lead with different profile
    print("\n\n🧪 TEST 2: Growth-Stage Startup Lead")
    print("-"*80)
    
    startup_lead = {
        "name": "Michael Chen",
        "email": "michael@aiventure.io",
        "company": "AIVenture Labs",
        "industry": "Artificial Intelligence",
        "employee_count": 32,
        "lead_message": "Exploring lead qualification automation for our sales team. "
                       "Early-stage exploration phase, not yet funded. Interested in demo.",
    }
    
    test_lead_analysis(startup_lead)
    
    # Test 3: Invalid data (will fail)
    print("\n\n🧪 TEST 3: Invalid Data (Missing Fields)")
    print("-"*80)
    
    invalid_lead = {
        "name": "John Doe",
        "email": "john@example.com",
        # Missing required fields
    }
    
    test_lead_analysis(invalid_lead)
    
    print("\n\n" + "="*80)
    print("✅ Testing completed!")
    print("="*80 + "\n")


def print_curl_examples():
    """Print curl command examples."""
    print("\n" + "="*80)
    print("📝 CURL COMMAND EXAMPLES")
    print("="*80 + "\n")
    
    curl_basic = '''
curl -X POST "http://localhost:8000/api/v1/leads/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "John Smith",
    "email": "john@company.com",
    "company": "Company Name",
    "industry": "Technology",
    "employee_count": 500,
    "lead_message": "We are interested in your AI solution for lead qualification."
  }'
'''
    
    print("📌 BASIC CURL REQUEST:")
    print(curl_basic)
    
    curl_with_output = '''
curl -X POST "http://localhost:8000/api/v1/leads/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{"name":"John","email":"john@test.com","company":"Test","industry":"Tech","employee_count":100,"lead_message":"Test"}' \\
  | python -m json.tool
'''
    
    print("\n📌 FORMATTED JSON OUTPUT:")
    print(curl_with_output)


def print_python_examples():
    """Print Python request examples."""
    print("\n" + "="*80)
    print("🐍 PYTHON REQUESTS EXAMPLES")
    print("="*80 + "\n")
    
    python_example = '''
import requests
import json

# Lead data
lead = {
    "name": "Alice Johnson",
    "email": "alice@company.com",
    "company": "Tech Corp",
    "industry": "Software",
    "employee_count": 250,
    "lead_message": "Looking for AI-powered lead qualification solution"
}

# Make request
response = requests.post(
    "http://localhost:8000/api/v1/leads/analyze",
    json=lead
)

# Handle response
if response.status_code == 200:
    result = response.json()
    analysis = result["analysis"]
    
    print(f"Summary: {analysis['summary']}")
    print(f"Budget: {analysis['budget']}")
    print(f"Timeline: {analysis['timeline']}")
    print(f"Pain Points: {analysis['pain_points']}")
else:
    print(f"Error: {response.json()}")
'''
    
    print(python_example)


if __name__ == "__main__":
    main()
    print_curl_examples()
    print_python_examples()
