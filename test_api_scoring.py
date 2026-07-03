#!/usr/bin/env python3
"""
API Testing for Lead Scoring Endpoint
=====================================

This file contains curl and Python examples for testing the lead scoring API.
"""

import requests
import json


# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://localhost:8000/api/v1"
ANALYSIS_ENDPOINT = f"{API_BASE_URL}/leads/analyze"
SCORING_ENDPOINT = f"{API_BASE_URL}/leads/score"

# Sample lead data
SAMPLE_LEAD = {
    "name": "Michael Johnson",
    "email": "michael.johnson@techventure.com",
    "company": "TechVenture Solutions",
    "industry": "Technology",
    "employee_count": 150,
    "lead_message": (
        "Hi, we're a mid-size tech company looking for AI solutions to streamline our operations. "
        "We have a budget of $75K-$125K and need this implemented by Q3 2024. "
        "Our main pain points are workflow automation and customer data management."
    )
}


# ============================================================================
# CURL EXAMPLES
# ============================================================================

CURL_ANALYZE = f"""
# Analyze Lead
curl -X POST {ANALYSIS_ENDPOINT} \\
  -H "Content-Type: application/json" \\
  -d '{{
    "name": "{SAMPLE_LEAD['name']}",
    "email": "{SAMPLE_LEAD['email']}",
    "company": "{SAMPLE_LEAD['company']}",
    "industry": "{SAMPLE_LEAD['industry']}",
    "employee_count": {SAMPLE_LEAD['employee_count']},
    "lead_message": "{SAMPLE_LEAD['lead_message']}"
  }}'
"""

CURL_SCORE = f"""
# Score Lead (use analysis from above)
curl -X POST {SCORING_ENDPOINT} \\
  -H "Content-Type: application/json" \\
  -d '{{
    "name": "{{analysis.name}}",
    "email": "{{analysis.email}}",
    "company": "{{analysis.company}}",
    "industry": "{{analysis.industry}}",
    "employee_count": {{analysis.employee_count}},
    "lead_message": "{{analysis.lead_message}}",
    "analysis": {{
      "summary": "{{analysis_result.summary}}",
      "requirement": "{{analysis_result.requirement}}",
      "budget": "{{analysis_result.budget}}",
      "timeline": "{{analysis_result.timeline}}",
      "urgency": "{{analysis_result.urgency}}",
      "company_size": "{{analysis_result.company_size}}",
      "industry": "{{analysis_result.industry}}",
      "pain_points": {{analysis_result.pain_points}}
    }}
  }}'
"""


# ============================================================================
# PYTHON EXAMPLES - SINGLE LEAD TESTING
# ============================================================================

def test_analyze_lead():
    """Test analyzing a single lead."""
    print("\n" + "=" * 80)
    print("TEST 1: Analyze Lead")
    print("=" * 80)
    
    try:
        print("\nURL:", ANALYSIS_ENDPOINT)
        print("\nRequest Body:")
        print(json.dumps(SAMPLE_LEAD, indent=2))
        
        response = requests.post(ANALYSIS_ENDPOINT, json=SAMPLE_LEAD)
        
        print(f"\nStatus Code: {response.status_code}")
        print("\nResponse:")
        print(json.dumps(response.json(), indent=2))
        
        return response.json()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("   Make sure the server is running: python -m backend.main")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return None


def test_score_lead(analysis_result):
    """Test scoring a lead using previous analysis results."""
    print("\n" + "=" * 80)
    print("TEST 2: Score Lead (using analysis from TEST 1)")
    print("=" * 80)
    
    if not analysis_result:
        print("\n⚠️  SKIPPED: No analysis result from TEST 1")
        return None
    
    try:
        # Prepare scoring request
        scoring_request = {
            **SAMPLE_LEAD,
            "analysis": analysis_result["analysis"]
        }
        
        print("\nURL:", SCORING_ENDPOINT)
        print("\nRequest Body:")
        print(json.dumps(scoring_request, indent=2))
        
        response = requests.post(SCORING_ENDPOINT, json=scoring_request)
        
        print(f"\nStatus Code: {response.status_code}")
        print("\nResponse:")
        response_data = response.json()
        print(json.dumps(response_data, indent=2))
        
        return response_data
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("   Make sure the server is running: python -m backend.main")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return None


# ============================================================================
# PYTHON EXAMPLES - MULTIPLE LEADS TESTING
# ============================================================================

SAMPLE_LEADS = [
    {
        "name": "Sarah Chen",
        "email": "sarah.chen@startup.io",
        "company": "StartupIO",
        "industry": "AI/ML",
        "employee_count": 30,
        "lead_message": (
            "Small startup exploring AI tools. Budget limited to $20K-$30K. "
            "Need something quickly - timeline is ASAP. Main pain: data processing."
        )
    },
    {
        "name": "Robert Williams",
        "email": "robert.williams@enterprise.com",
        "company": "Enterprise Corp",
        "industry": "Finance",
        "employee_count": 5000,
        "lead_message": (
            "Large enterprise seeking comprehensive platform. Budget $500K+. "
            "Flexible on timeline but prefer Q4 implementation. Multiple departments involved."
        )
    },
    {
        "name": "Amanda Rodriguez",
        "email": "amanda.rodriguez@midmarket.biz",
        "company": "MidMarket Services",
        "industry": "Consulting",
        "employee_count": 250,
        "lead_message": (
            "Mid-market firm evaluating options. Budget $100K-$200K. Timeline TBD. "
            "Still in discovery phase, comparing 3 vendors."
        )
    },
]


def test_batch_analysis_and_scoring():
    """Test analyzing and scoring multiple leads."""
    print("\n" + "=" * 80)
    print("TEST 3: Batch Analysis & Scoring")
    print("=" * 80)
    
    results = []
    
    for i, lead in enumerate(SAMPLE_LEADS, 1):
        print(f"\n--- Processing Lead {i}/{len(SAMPLE_LEADS)}: {lead['company']} ---")
        
        try:
            # Analyze
            print("  Analyzing...")
            analysis_response = requests.post(ANALYSIS_ENDPOINT, json=lead)
            
            if analysis_response.status_code != 200:
                print(f"  ❌ Analysis failed: {analysis_response.status_code}")
                continue
            
            analysis_data = analysis_response.json()
            
            # Score
            print("  Scoring...")
            scoring_request = {
                **lead,
                "analysis": analysis_data["analysis"]
            }
            
            scoring_response = requests.post(SCORING_ENDPOINT, json=scoring_request)
            
            if scoring_response.status_code != 200:
                print(f"  ❌ Scoring failed: {scoring_response.status_code}")
                continue
            
            scoring_data = scoring_response.json()
            
            # Extract key metrics
            score = scoring_data["scoring"]["lead_score"]
            priority = scoring_data["scoring"]["priority"]
            confidence = scoring_data["scoring"]["confidence"]
            
            print(f"  ✓ Score: {score}/100 | Priority: {priority} | Confidence: {confidence}%")
            
            results.append({
                "company": lead["company"],
                "score": score,
                "priority": priority,
                "confidence": confidence,
            })
            
        except requests.exceptions.ConnectionError:
            print("  ❌ ERROR: Could not connect to API")
            break
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            continue
    
    # Display summary
    if results:
        print("\n" + "-" * 80)
        print("SUMMARY - Leads Ranked by Score")
        print("-" * 80)
        
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
        
        for rank, result in enumerate(sorted_results, 1):
            symbol = "🔥" if result["priority"] == "Hot" else "🔶" if result["priority"] == "Warm" else "❄️"
            print(
                f"{rank}. {symbol} {result['company']:<30} "
                f"Score: {result['score']:>3}/100  "
                f"Confidence: {result['confidence']:>3}%"
            )
        
        # Priority breakdown
        print("\nPriority Breakdown:")
        hot = sum(1 for r in results if r["priority"] == "Hot")
        warm = sum(1 for r in results if r["priority"] == "Warm")
        cold = sum(1 for r in results if r["priority"] == "Cold")
        print(f"  🔥 Hot:  {hot}")
        print(f"  🔶 Warm: {warm}")
        print(f"  ❄️ Cold:  {cold}")


# ============================================================================
# ERROR TESTING
# ============================================================================

def test_error_scenarios():
    """Test various error scenarios."""
    print("\n" + "=" * 80)
    print("TEST 4: Error Scenarios")
    print("=" * 80)
    
    # Test 1: Missing required field
    print("\n--- Error Test 1: Missing Required Field ---")
    invalid_lead = {"name": "John Doe"}  # Missing email, company, etc.
    response = requests.post(ANALYSIS_ENDPOINT, json=invalid_lead)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Invalid email
    print("\n--- Error Test 2: Invalid Email Format ---")
    invalid_email_lead = {
        **SAMPLE_LEAD,
        "email": "not-an-email"
    }
    response = requests.post(ANALYSIS_ENDPOINT, json=invalid_email_lead)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Invalid employee count
    print("\n--- Error Test 3: Invalid Employee Count ---")
    invalid_count_lead = {
        **SAMPLE_LEAD,
        "employee_count": -5
    }
    response = requests.post(ANALYSIS_ENDPOINT, json=invalid_count_lead)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "LEAD SCORING API ENDPOINT TESTS" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")
    
    print("\n📌 CURL EXAMPLES")
    print("=" * 80)
    print("\nAnalyze Lead:")
    print(CURL_ANALYZE)
    print("\nScore Lead:")
    print(CURL_SCORE)
    
    print("\n📌 PYTHON TESTS")
    print("=" * 80)
    print("\nMaking sure the API is running on http://localhost:8000")
    print("If not, start the server with: python -m backend.main")
    
    # Run tests
    analysis_result = test_analyze_lead()
    
    if analysis_result:
        scoring_result = test_score_lead(analysis_result)
    
    test_batch_analysis_and_scoring()
    
    test_error_scenarios()
    
    # Final instructions
    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
    print("\n✓ Analysis & Scoring endpoints tested")
    print("✓ Check responses for correctness")
    print("✓ Verify priority levels match expected ranges")
    print("\nNext steps:")
    print("1. Review scoring results for accuracy")
    print("2. Integrate with sales workflow")
    print("3. Monitor API performance")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
