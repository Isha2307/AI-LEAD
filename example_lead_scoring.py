"""
Lead Scoring Agent - Complete Implementation Example
====================================================

This example demonstrates the complete workflow of analyzing and scoring leads:
1. Analyze lead data
2. Score the lead based on analysis
3. Get recommendations and priority levels
"""

import json
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(__file__).rsplit('\\', 2)[0])

from backend.agents import lead_analyzer_agent, lead_scoring_agent
from backend.schemas import LeadAnalysisRequest


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Print a formatted section."""
    print(f"\n  {title}")
    print("  " + "-" * 76)


def score_single_lead():
    """Analyze and score a single lead - complete workflow."""
    print_header("SINGLE LEAD ANALYSIS & SCORING EXAMPLE")
    
    # Sample lead data
    lead_data = {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@techcorp.com",
        "company": "TechCorp Solutions",
        "industry": "Technology",
        "employee_count": 250,
        "lead_message": (
            "Hi, we're currently evaluating AI solutions for our enterprise operations. "
            "We have a budget of $200K-$300K and need implementation within Q3 2024. "
            "Our main pain points are process automation and data integration."
        )
    }
    
    print_section("STEP 1: Lead Data Input")
    print(f"  Name: {lead_data['name']}")
    print(f"  Email: {lead_data['email']}")
    print(f"  Company: {lead_data['company']}")
    print(f"  Industry: {lead_data['industry']}")
    print(f"  Employees: {lead_data['employee_count']}")
    print(f"  Message: {lead_data['lead_message'][:60]}...")
    
    try:
        # Step 1: Analyze the lead
        print_section("STEP 2: Lead Analysis (Gemini AI)")
        
        if not lead_analyzer_agent:
            print("  ❌ ERROR: Lead analyzer agent not available")
            print("     Please check GEMINI_API_KEY configuration")
            return
        
        analysis = lead_analyzer_agent.analyze_lead(
            name=lead_data["name"],
            email=lead_data["email"],
            company=lead_data["company"],
            industry=lead_data["industry"],
            employee_count=lead_data["employee_count"],
            lead_message=lead_data["lead_message"],
        )
        
        print(f"  ✓ Analysis successful")
        print(f"  • Summary: {analysis.summary[:100]}...")
        print(f"  • Budget: {analysis.budget}")
        print(f"  • Timeline: {analysis.timeline}")
        print(f"  • Urgency: {analysis.urgency}")
        print(f"  • Company Size: {analysis.company_size}")
        print(f"  • Pain Points: {', '.join(analysis.pain_points[:2])}...")
        
        # Step 2: Score the lead
        print_section("STEP 3: Lead Scoring (Gemini AI)")
        
        if not lead_scoring_agent:
            print("  ❌ ERROR: Lead scoring agent not available")
            print("     Please check GEMINI_API_KEY configuration")
            return
        
        scoring = lead_scoring_agent.score_lead(
            name=lead_data["name"],
            email=lead_data["email"],
            company=lead_data["company"],
            industry=lead_data["industry"],
            employee_count=lead_data["employee_count"],
            lead_message=lead_data["lead_message"],
            analysis=analysis,
        )
        
        print(f"  ✓ Scoring successful")
        print(f"  • Lead Score: {scoring.lead_score}/100")
        print(f"  • Priority: {scoring.priority}")
        print(f"  • Confidence: {scoring.confidence}%")
        
        print_section("STEP 4: Reasoning")
        for i, reason in enumerate(scoring.reasoning, 1):
            print(f"  {i}. {reason}")
        
        # Get recommendation
        print_section("STEP 5: Recommended Action")
        recommendation = lead_scoring_agent.get_action_recommendation(scoring)
        print(f"  {recommendation}")
        
        # Display complete results
        print_section("COMPLETE RESULTS (JSON)")
        results = {
            "lead": lead_data,
            "analysis": analysis.model_dump(),
            "scoring": scoring.model_dump(),
            "recommendation": recommendation,
            "timestamp": datetime.utcnow().isoformat(),
        }
        print(json.dumps(results, indent=2))
        
        return results
        
    except Exception as e:
        print(f"\n  ❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def score_multiple_leads():
    """Analyze and score multiple leads - batch processing."""
    print_header("BATCH LEAD ANALYSIS & SCORING EXAMPLE")
    
    leads = [
        {
            "name": "John Smith",
            "email": "john.smith@startup.io",
            "company": "StartupIO",
            "industry": "AI/ML",
            "employee_count": 45,
            "lead_message": (
                "We're a startup looking for AI solutions. Our budget is tight ($30K-$50K) "
                "but we have urgent needs. Implementation needed ASAP."
            )
        },
        {
            "name": "Maria Garcia",
            "email": "maria.garcia@enterprise.com",
            "company": "Enterprise Corp",
            "industry": "Finance",
            "employee_count": 5000,
            "lead_message": (
                "Large enterprise seeking comprehensive platform. Budget $500K+. "
                "Timeline flexible, Q4 implementation acceptable. Multiple departments impacted."
            )
        },
        {
            "name": "Mike Chen",
            "email": "mike.chen@midmarket.biz",
            "company": "MidMarket Inc",
            "industry": "Manufacturing",
            "employee_count": 300,
            "lead_message": (
                "Mid-market company exploring options. Currently evaluating 3 vendors. "
                "Budget $100K-$150K. Timeline unclear, still in discovery phase."
            )
        },
    ]
    
    print(f"  Processing {len(leads)} leads for analysis and scoring...")
    
    if not lead_analyzer_agent or not lead_scoring_agent:
        print("  ❌ ERROR: Agents not available. Check GEMINI_API_KEY configuration.")
        return
    
    all_results = []
    
    try:
        for i, lead in enumerate(leads, 1):
            print(f"\n  Processing lead {i}/{len(leads)}: {lead['company']}...")
            
            # Analyze lead
            analysis = lead_analyzer_agent.analyze_lead(
                name=lead["name"],
                email=lead["email"],
                company=lead["company"],
                industry=lead["industry"],
                employee_count=lead["employee_count"],
                lead_message=lead["lead_message"],
            )
            
            # Score lead
            scoring = lead_scoring_agent.score_lead(
                name=lead["name"],
                email=lead["email"],
                company=lead["company"],
                industry=lead["industry"],
                employee_count=lead["employee_count"],
                lead_message=lead["lead_message"],
                analysis=analysis,
            )
            
            result = {
                "company": lead["company"],
                "score": scoring.lead_score,
                "priority": scoring.priority,
                "confidence": scoring.confidence,
            }
            
            all_results.append(result)
            print(f"    • Score: {scoring.lead_score}/100 | Priority: {scoring.priority} | Confidence: {scoring.confidence}%")
        
        # Sort by score (high to low)
        print_section("SUMMARY - Leads Ranked by Score")
        sorted_results = sorted(all_results, key=lambda x: x["score"], reverse=True)
        
        for rank, result in enumerate(sorted_results, 1):
            priority_symbol = "🔥" if result["priority"] == "Hot" else "🔶" if result["priority"] == "Warm" else "❄️"
            print(f"  {rank}. {priority_symbol} {result['company']:<25} Score: {result['score']:>3}/100  Confidence: {result['confidence']:>3}%")
        
        # Priority breakdown
        print_section("PRIORITY BREAKDOWN")
        hot_count = sum(1 for r in all_results if r["priority"] == "Hot")
        warm_count = sum(1 for r in all_results if r["priority"] == "Warm")
        cold_count = sum(1 for r in all_results if r["priority"] == "Cold")
        
        print(f"  🔥 Hot (Ready for immediate follow-up):    {hot_count}")
        print(f"  🔶 Warm (Needs investigation):             {warm_count}")
        print(f"  ❄️ Cold (Nurture track):                   {cold_count}")
        
        return sorted_results
        
    except Exception as e:
        print(f"\n  ❌ ERROR during batch processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def demonstrate_scoring_ranges():
    """Demonstrate scoring ranges and priority levels."""
    print_header("SCORING RANGES & PRIORITY LEVELS")
    
    ranges = [
        (80, 100, "Hot", "🔥", "Immediate action required. High fit, urgent need, good budget, near timeline."),
        (50, 79, "Warm", "🔶", "Investigation recommended. Medium fit, potential opportunity, follow up for details."),
        (0, 49, "Cold", "❄️", "Lower priority. Poor fit or insufficient information. Add to nurture campaign."),
    ]
    
    for min_score, max_score, priority, symbol, description in ranges:
        print(f"\n  {symbol} {priority} ({min_score}-{max_score})")
        print(f"     {description}")
    
    print_section("SCORING FACTORS")
    print("  The AI considers multiple factors when scoring:")
    print("  • Budget indicators (budget range and company size)")
    print("  • Timeline urgency (implementation timeline)")
    print("  • Urgency level (how quickly they need a solution)")
    print("  • Pain points (number and severity of identified issues)")
    print("  • Engagement signals (tone and clarity of message)")
    print("  • Industry match (relevance to typical use cases)")
    print("  • Company characteristics (employee count, sector)")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "LEAD SCORING AGENT - COMPLETE WORKFLOW EXAMPLES" + " " * 17 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Run examples
    single_result = score_single_lead()
    
    batch_result = score_multiple_leads()
    
    demonstrate_scoring_ranges()
    
    # Final summary
    print_header("SUMMARY")
    print("  ✓ Lead Analysis Agent: Extracts structured insights from lead data")
    print("  ✓ Lead Scoring Agent: Prioritizes leads for sales action")
    print("  ✓ Combined: Complete workflow from raw lead to prioritized opportunity")
    print("\n  The LeadScoringAgent provides:")
    print("  • Numerical scores (0-100) for consistent comparison")
    print("  • Priority levels (Hot/Warm/Cold) for quick triage")
    print("  • Confidence ratings for assessment reliability")
    print("  • Detailed reasoning for transparent decision-making")
    print("\n  Use the API endpoints:")
    print("  • POST /api/v1/leads/analyze - Analyze lead data")
    print("  • POST /api/v1/leads/score - Score analyzed lead")
    print("\n")


if __name__ == "__main__":
    main()
