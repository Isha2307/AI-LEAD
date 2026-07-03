"""
Three-Agent Integration Example
================================

Complete demonstration of the Lead Qualification & Follow-up System
with all three agents working together in a unified workflow:

1. Lead Analysis → Extract structured data
2. Lead Scoring → Prioritize leads
3. Email Generation → Create personalized follow-up emails
"""

import json
import sys
from datetime import datetime

sys.path.insert(0, str(__file__).rsplit('\\', 2)[0])

from backend.agents import (
    lead_analysis_agent,
    lead_scoring_agent,
    email_generator_agent,
)


def print_header(title):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Print formatted section."""
    print(f"\n  {title}")
    print("  " + "-" * 76)


def format_lead_data(lead: dict) -> str:
    """Format lead data as JSON string for analysis."""
    return json.dumps(lead, indent=2)


def process_single_lead(lead_data: dict) -> dict:
    """
    Process a single lead through all three agents.
    
    Returns: Dictionary with analysis, scoring, and email generation results
    """
    company = lead_data.get("company", "Unknown")
    name = lead_data.get("name", "Unknown")
    
    print_header(f"PROCESSING LEAD: {name} @ {company}")
    
    results = {
        "lead_data": lead_data,
        "analysis": None,
        "scoring": None,
        "email": None,
        "errors": []
    }
    
    # Step 1: Lead Analysis
    print_section("STEP 1: LEAD ANALYSIS")
    print(f"  Input: Raw lead data for {name}")
    
    try:
        if not lead_analysis_agent:
            results["errors"].append("Lead analysis agent not available")
            print("  ❌ Lead analysis agent not available")
            return results
        
        # Format lead data as JSON for analysis
        lead_json = format_lead_data(lead_data)
        
        print(f"  Analyzing lead information...")
        analysis_result = lead_analysis_agent.analyze_lead(lead_json)
        
        results["analysis"] = {
            "company_name": analysis_result.company_name,
            "industry": analysis_result.industry,
            "pain_points": analysis_result.pain_points,
            "technology_stack": analysis_result.technology_stack,
            "estimated_budget": analysis_result.estimated_budget,
            "decision_timeline": analysis_result.decision_timeline,
            "key_decision_makers": analysis_result.key_decision_makers,
            "engagement_level": analysis_result.engagement_level,
        }
        
        print(f"  ✓ Analysis complete")
        print(f"    • Company: {analysis_result.company_name}")
        print(f"    • Industry: {analysis_result.industry}")
        print(f"    • Pain Points: {analysis_result.pain_points[:50]}...")
        print(f"    • Budget: {analysis_result.estimated_budget}")
        print(f"    • Timeline: {analysis_result.decision_timeline}")
        
    except Exception as e:
        error_msg = f"Lead analysis failed: {str(e)}"
        results["errors"].append(error_msg)
        print(f"  ❌ {error_msg}")
        return results
    
    # Step 2: Lead Scoring
    print_section("STEP 2: LEAD SCORING & PRIORITIZATION")
    print(f"  Input: Analysis results from Step 1")
    
    try:
        if not lead_scoring_agent:
            results["errors"].append("Lead scoring agent not available")
            print("  ❌ Lead scoring agent not available")
            return results
        
        print(f"  Scoring lead based on analysis...")
        scoring_result = lead_scoring_agent.score_lead(analysis_result)
        
        results["scoring"] = {
            "score": scoring_result.score,
            "priority": scoring_result.priority,
            "confidence": scoring_result.confidence,
            "reasoning": scoring_result.reasoning,
        }
        
        print(f"  ✓ Scoring complete")
        print(f"    • Score: {scoring_result.score}/100")
        print(f"    • Priority: {scoring_result.priority}")
        print(f"    • Confidence: {scoring_result.confidence}%")
        print(f"    • Reasoning: {scoring_result.reasoning[:70]}...")
        
    except Exception as e:
        error_msg = f"Lead scoring failed: {str(e)}"
        results["errors"].append(error_msg)
        print(f"  ❌ {error_msg}")
        return results
    
    # Step 3: Email Generation (if Hot or Warm)
    print_section("STEP 3: EMAIL GENERATION")
    
    if scoring_result.priority not in ["Hot", "Warm", "Cold"]:
        print(f"  ⚠ Invalid priority: {scoring_result.priority}")
        return results
    
    # Determine if we should generate email
    if scoring_result.score < 20:
        print(f"  ⊘ Score too low ({scoring_result.score}/100) - skipping email generation")
        print(f"    Consider nurturing this lead for future outreach")
        return results
    
    try:
        if not email_generator_agent:
            results["errors"].append("Email generation agent not available")
            print("  ❌ Email generation agent not available")
            return results
        
        print(f"  Generating {scoring_result.priority} priority email...")
        print(f"  Input:")
        print(f"    • Company: {analysis_result.company_name}")
        print(f"    • Requirement: {analysis_result.pain_points[:50]}...")
        print(f"    • Budget: {analysis_result.estimated_budget}")
        print(f"    • Timeline: {analysis_result.decision_timeline}")
        print(f"    • Priority: {scoring_result.priority}")
        
        email_result = email_generator_agent.generate_email(
            company=analysis_result.company_name,
            requirement=analysis_result.pain_points,
            budget=analysis_result.estimated_budget,
            timeline=analysis_result.decision_timeline,
            priority=scoring_result.priority,
        )
        
        results["email"] = {
            "subject": email_result.subject,
            "body": email_result.email,
            "priority": scoring_result.priority,
        }
        
        print(f"  ✓ Email generated successfully")
        print(f"    • Subject: {email_result.subject}")
        print(f"    • Body length: {len(email_result.email)} characters")
        
    except Exception as e:
        error_msg = f"Email generation failed: {str(e)}"
        results["errors"].append(error_msg)
        print(f"  ❌ {error_msg}")
    
    return results


def process_lead_batch(leads: list) -> list:
    """Process multiple leads through the complete workflow."""
    print_header("BATCH LEAD PROCESSING - MULTIPLE LEADS")
    
    print(f"  Processing {len(leads)} leads through the complete workflow...\n")
    
    results = []
    stats = {
        "total": len(leads),
        "analyzed": 0,
        "scored": 0,
        "hot": 0,
        "warm": 0,
        "cold": 0,
        "emails_generated": 0,
        "errors": 0,
    }
    
    for i, lead in enumerate(leads, 1):
        print(f"\n┌─ LEAD {i}/{len(leads)} ─────────────────────────────────────────────────────┐")
        
        result = process_single_lead(lead)
        results.append(result)
        
        if result["analysis"]:
            stats["analyzed"] += 1
        if result["scoring"]:
            stats["scored"] += 1
            priority = result["scoring"]["priority"]
            if priority == "Hot":
                stats["hot"] += 1
            elif priority == "Warm":
                stats["warm"] += 1
            else:
                stats["cold"] += 1
        if result["email"]:
            stats["emails_generated"] += 1
        if result["errors"]:
            stats["errors"] += len(result["errors"])
        
        print("\n└─────────────────────────────────────────────────────────────────────────────┘")
    
    # Print summary
    print_header("BATCH PROCESSING SUMMARY")
    print(f"  Leads Processed:")
    print(f"    Total: {stats['total']}")
    print(f"    ✓ Analyzed: {stats['analyzed']}")
    print(f"    ✓ Scored: {stats['scored']}")
    print(f"    ✗ Errors: {stats['errors']}")
    
    print(f"\n  Priority Distribution:")
    print(f"    🔥 Hot (80-100): {stats['hot']}")
    print(f"    🔶 Warm (50-79): {stats['warm']}")
    print(f"    ❄️ Cold (0-49): {stats['cold']}")
    
    print(f"\n  Email Generation:")
    print(f"    ✓ Emails Generated: {stats['emails_generated']}")
    print(f"    ⊘ Skipped: {stats['analyzed'] - stats['emails_generated']}")
    
    return results


def display_email_with_context(result: dict):
    """Display full email with lead context."""
    if not result["email"]:
        return
    
    analysis = result["analysis"]
    scoring = result["scoring"]
    email = result["email"]
    lead_data = result["lead_data"]
    
    print_header(f"FINAL EMAIL - {lead_data.get('name')} @ {analysis['company_name']}")
    
    # Email header
    print("  ┌─ EMAIL PREVIEW ──────────────────────────────────────────────────────────┐")
    print(f"  │ To: {lead_data.get('email', 'user@company.com'):<70} │")
    print(f"  │ Subject: {email['subject']:<62} │")
    print(f"  │ Priority: {scoring['priority']:<63} │")
    print(f"  │ Score: {scoring['score']}/100, Confidence: {scoring['confidence']}%{' ':<30} │")
    print("  ├─ BODY ────────────────────────────────────────────────────────────────────┤")
    
    # Email body with wrapping
    lines = email['body'].split('\n')
    for line in lines:
        if len(line) > 74:
            words = line.split(' ')
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= 74:
                    current_line += word + " "
                else:
                    if current_line:
                        print(f"  │ {current_line:<74} │")
                    current_line = word + " "
            if current_line:
                print(f"  │ {current_line:<74} │")
        else:
            print(f"  │ {line:<74} │")
    
    print("  └─────────────────────────────────────────────────────────────────────────────┘")
    
    # Context information
    print_section("Lead Context")
    print(f"  Industry: {analysis['industry']}")
    print(f"  Pain Points: {analysis['pain_points'][:60]}...")
    print(f"  Decision Timeline: {analysis['decision_timeline']}")
    print(f"  Estimated Budget: {analysis['estimated_budget']}")
    print(f"  Engagement Level: {analysis['engagement_level']}")


def main():
    """Main demonstration."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "THREE-AGENT INTEGRATION DEMONSTRATION" + " " * 27 + "║")
    print("║" + " " * 13 + "Lead Analysis + Scoring + Email Generation" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Example leads
    example_leads = [
        {
            "name": "John Smith",
            "title": "VP of Operations",
            "company": "TechCorp Solutions",
            "email": "john.smith@techcorp.com",
            "recent_activity": "Downloaded AI implementation guide, attended webinar",
            "company_size": "500+ employees",
            "annual_revenue": "$100M+",
            "pain_points": "Struggling with manual customer support processes, high operational costs",
        },
        {
            "name": "Sarah Johnson",
            "title": "Director of Technology",
            "company": "FinServe Inc",
            "email": "sarah.j@finserve.com",
            "recent_activity": "Requested demo, visited pricing page multiple times",
            "company_size": "100-500 employees",
            "annual_revenue": "$50M-$100M",
            "pain_points": "Need better data integration for compliance reporting",
        },
        {
            "name": "Mike Chen",
            "title": "CEO",
            "company": "StartupXYZ",
            "email": "mike@startupxyz.io",
            "recent_activity": "Read blog post, no follow-up",
            "company_size": "<50 employees",
            "annual_revenue": "$1M-$5M",
            "pain_points": "Exploring AI tools but budget is limited",
        },
    ]
    
    # Process leads
    results = process_lead_batch(example_leads)
    
    # Display detailed results
    print_header("DETAILED RESULTS")
    
    for i, result in enumerate(results, 1):
        if result["email"]:
            display_email_with_context(result)
    
    # Final summary
    print_header("SYSTEM CAPABILITIES")
    print("  ✓ Lead Analysis Agent")
    print("    • Extracts structured data from raw lead information")
    print("    • Identifies industry, pain points, budget, timeline")
    print("    • Uses Gemini AI for intelligent extraction")
    
    print("\n  ✓ Lead Scoring Agent")
    print("    • Prioritizes leads with 0-100 score")
    print("    • Assigns priority: Hot (80-100), Warm (50-79), Cold (0-49)")
    print("    • Provides confidence score and reasoning")
    
    print("\n  ✓ Email Generation Agent")
    print("    • Generates personalized B2B sales follow-up emails")
    print("    • Adapts tone based on lead priority")
    print("    • Creates professional subject lines and email bodies")
    
    print("\n  ✓ Complete Workflow")
    print("    • Seamless integration of all three agents")
    print("    • Leads flow through analysis → scoring → email")
    print("    • Batch processing for multiple leads efficiently")
    
    print("\n  ✓ API Endpoints Available")
    print("    • POST /api/v1/leads/analyze")
    print("    • POST /api/v1/leads/score")
    print("    • POST /api/v1/leads/generate-email")
    
    print("\n")


if __name__ == "__main__":
    main()
