"""
Example script demonstrating lead analysis functionality.

This script shows how to:
1. Initialize the lead analyzer agent
2. Analyze a lead with the Gemini API
3. Handle the structured JSON response
4. Access qualification insights

To run this script:
1. Set up environment variables (.env file with GEMINI_API_KEY)
2. Run: python example_lead_analysis.py

Example output will show the analyzed lead with all extracted fields.
"""

import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.agents import lead_analyzer_agent
from backend.utils import app_logger


def example_lead_analysis():
    """
    Demonstrate lead analysis with a sample lead.
    """
    if not lead_analyzer_agent:
        print("❌ INITIALIZATION ERROR")
        print("LeadAnalysisAgent is not available.")
        print("Please ensure GEMINI_API_KEY is set in .env file")
        return
    
    # Sample lead data
    sample_lead = {
        "name": "John Smith",
        "email": "john.smith@techcorp.com",
        "company": "TechCorp Solutions",
        "industry": "Software/Technology",
        "employee_count": 250,
        "lead_message": "We're looking for an AI-powered lead qualification solution to automate our sales process. "
                       "Our team is spending too much time on manual lead scoring. We need something that can "
                       "integrate with our existing CRM and provide real-time insights.",
    }
    
    print("\n" + "="*80)
    print("🤖 AI LEAD ANALYSIS AGENT - EXAMPLE")
    print("="*80)
    
    print("\n📋 INPUT LEAD DATA:")
    print("-" * 80)
    for key, value in sample_lead.items():
        if key != "lead_message":
            print(f"  {key.capitalize()}: {value}")
        else:
            print(f"  {key.capitalize()}: {value[:80]}...")
    
    print("\n⏳ Analyzing lead with Gemini API...")
    print("-" * 80)
    
    try:
        # Analyze the lead
        analysis = lead_analyzer_agent.analyze_lead(
            name=sample_lead["name"],
            email=sample_lead["email"],
            company=sample_lead["company"],
            industry=sample_lead["industry"],
            employee_count=sample_lead["employee_count"],
            lead_message=sample_lead["lead_message"],
        )
        
        # Get qualification score
        score, is_qualified = lead_analyzer_agent.get_qualification_score(analysis)
        
        # Display results
        print("\n✅ ANALYSIS RESULTS:")
        print("-" * 80)
        
        print(f"\n📊 QUALIFICATION SCORE: {score:.1f}/100")
        print(f"✨ IS QUALIFIED: {'YES ✓' if is_qualified else 'NO ✗'}")
        
        print(f"\n📝 SUMMARY:")
        print(f"   {analysis.summary}")
        
        print(f"\n🎯 REQUIREMENT:")
        print(f"   {analysis.requirement}")
        
        print(f"\n💰 BUDGET:")
        print(f"   {analysis.budget}")
        
        print(f"\n📅 TIMELINE:")
        print(f"   {analysis.timeline}")
        
        print(f"\n⚡ URGENCY:")
        print(f"   {analysis.urgency}")
        
        print(f"\n🏢 COMPANY SIZE:")
        print(f"   {analysis.company_size}")
        
        print(f"\n🏭 INDUSTRY:")
        print(f"   {analysis.industry}")
        
        print(f"\n💭 IDENTIFIED PAIN POINTS:")
        for i, pain_point in enumerate(analysis.pain_points, 1):
            print(f"   {i}. {pain_point}")
        
        # Raw JSON output
        print("\n\n📦 RAW JSON OUTPUT:")
        print("-" * 80)
        print(json.dumps(analysis.model_dump(), indent=2))
        
        print("\n" + "="*80)
        print("✅ Analysis completed successfully!")
        print("="*80 + "\n")
        
    except ValueError as e:
        print(f"\n❌ VALIDATION ERROR:")
        print(f"   {str(e)}")
        print("\n   Please check that all required fields are properly filled.")
        
    except RuntimeError as e:
        print(f"\n❌ GEMINI API ERROR:")
        print(f"   {str(e)}")
        print("\n   Please check:")
        print("   - GEMINI_API_KEY is set in .env")
        print("   - API key is valid and has active quota")
        print("   - Network connection is available")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()


def example_batch_analysis():
    """
    Demonstrate batch analysis of multiple leads.
    """
    if not lead_analyzer_agent:
        print("❌ LeadAnalysisAgent not initialized")
        return
    
    # Sample leads
    leads = [
        {
            "name": "Alice Johnson",
            "email": "alice@startup.io",
            "company": "StartupIO",
            "industry": "Fintech",
            "employee_count": 45,
            "lead_message": "Interested in scaling our sales team with AI tools.",
        },
        {
            "name": "Bob Wilson",
            "email": "bob@enterprise.com",
            "company": "EnterpriseGlobal",
            "industry": "Manufacturing",
            "employee_count": 5000,
            "lead_message": "Need enterprise solution for lead management across 50+ sales reps.",
        },
    ]
    
    print("\n" + "="*80)
    print("🤖 BATCH LEAD ANALYSIS - EXAMPLE")
    print("="*80)
    
    print(f"\n📊 Analyzing {len(leads)} leads...")
    print("-" * 80)
    
    try:
        results = lead_analyzer_agent.batch_analyze_leads(leads)
        
        # Display summary
        successful = sum(1 for r in results if r["status"] == "success")
        failed = sum(1 for r in results if r["status"] == "failed")
        
        print(f"\n✅ BATCH RESULTS:")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        
        for i, result in enumerate(results, 1):
            print(f"\n   Lead {i}: {result['lead']['name']}")
            if result["status"] == "success":
                score, is_qualified = lead_analyzer_agent.get_qualification_score(
                    type('obj', (object,), result['analysis'])()
                )
                print(f"      Score: {score:.1f}/100 | Qualified: {is_qualified}")
            else:
                print(f"      Error: {result['error']}")
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during batch analysis: {str(e)}")


if __name__ == "__main__":
    print("\n🚀 LEAD ANALYSIS AGENT EXAMPLES\n")
    
    # Run single lead analysis
    example_lead_analysis()
    
    # Uncomment to run batch analysis
    # example_batch_analysis()
    
    print("\n✨ Examples completed!\n")
