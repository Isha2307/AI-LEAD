"""
Email Generation Agent - Complete Implementation Example
========================================================

This example demonstrates the EmailGenerationAgent for creating personalized
B2B sales follow-up emails based on lead information and priority levels.
"""

import json
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(__file__).rsplit('\\', 2)[0])

from backend.agents import email_generator_agent


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Print a formatted section."""
    print(f"\n  {title}")
    print("  " + "-" * 76)


def print_email(subject, email_body):
    """Print formatted email."""
    print("\n  ┌──────────────────────────────────────────────────────────────────────────┐")
    print(f"  │ To: [prospect@company.com]                                              │")
    print(f"  │ Subject: {subject:<64} │")
    print("  ├──────────────────────────────────────────────────────────────────────────┤")
    
    # Split email into lines and print with wrapping
    lines = email_body.split('\n')
    for line in lines:
        # Wrap long lines
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
    
    print("  └──────────────────────────────────────────────────────────────────────────┘")


def generate_hot_lead_email():
    """Generate email for a Hot lead (immediate action needed)."""
    print_header("EMAIL GENERATION - HOT LEAD (Immediate Action)")
    
    company = "TechCorp Solutions"
    requirement = "Enterprise AI platform for automating customer support processes"
    budget = "$200K-$500K"
    timeline = "Q2 2024 (immediate implementation)"
    priority = "Hot"
    
    print_section("Lead Information")
    print(f"  Company:    {company}")
    print(f"  Priority:   {priority} 🔥")
    print(f"  Requirement: {requirement}")
    print(f"  Budget:     {budget}")
    print(f"  Timeline:   {timeline}")
    
    try:
        if not email_generator_agent:
            print("\n  ❌ ERROR: Email generator agent not available")
            print("     Please check GEMINI_API_KEY configuration")
            return None
        
        print_section("Generating Email via Gemini AI")
        
        email_result = email_generator_agent.generate_email(
            company=company,
            requirement=requirement,
            budget=budget,
            timeline=timeline,
            priority=priority,
        )
        
        print(f"  ✓ Email generated successfully")
        
        print_section("Generated Email")
        print_email(email_result.subject, email_result.email)
        
        print_section("Tone and Approach")
        guidance = email_generator_agent.get_email_tone_guidance(priority)
        print(f"  {guidance}")
        
        return {
            "company": company,
            "priority": priority,
            "subject": email_result.subject,
            "email": email_result.email,
            "guidance": guidance,
        }
        
    except Exception as e:
        print(f"\n  ❌ ERROR: {str(e)}")
        return None


def generate_warm_lead_email():
    """Generate email for a Warm lead (investigation needed)."""
    print_header("EMAIL GENERATION - WARM LEAD (Investigation Phase)")
    
    company = "FinServe Inc"
    requirement = "Data integration and analytics platform for compliance reporting"
    budget = "$75K-$125K"
    timeline = "Q3 2024 (3-4 months)"
    priority = "Warm"
    
    print_section("Lead Information")
    print(f"  Company:    {company}")
    print(f"  Priority:   {priority} 🔶")
    print(f"  Requirement: {requirement}")
    print(f"  Budget:     {budget}")
    print(f"  Timeline:   {timeline}")
    
    try:
        if not email_generator_agent:
            print("\n  ❌ ERROR: Email generator agent not available")
            return None
        
        print_section("Generating Email via Gemini AI")
        
        email_result = email_generator_agent.generate_email(
            company=company,
            requirement=requirement,
            budget=budget,
            timeline=timeline,
            priority=priority,
        )
        
        print(f"  ✓ Email generated successfully")
        
        print_section("Generated Email")
        print_email(email_result.subject, email_result.email)
        
        print_section("Tone and Approach")
        guidance = email_generator_agent.get_email_tone_guidance(priority)
        print(f"  {guidance}")
        
        return {
            "company": company,
            "priority": priority,
            "subject": email_result.subject,
            "email": email_result.email,
            "guidance": guidance,
        }
        
    except Exception as e:
        print(f"\n  ❌ ERROR: {str(e)}")
        return None


def generate_cold_lead_email():
    """Generate email for a Cold lead (nurture track)."""
    print_header("EMAIL GENERATION - COLD LEAD (Nurture Track)")
    
    company = "StartupXYZ"
    requirement = "Initial exploration of AI solutions for early-stage startup"
    budget = "$20K-$30K (uncertain)"
    timeline = "Not defined yet"
    priority = "Cold"
    
    print_section("Lead Information")
    print(f"  Company:    {company}")
    print(f"  Priority:   {priority} ❄️")
    print(f"  Requirement: {requirement}")
    print(f"  Budget:     {budget}")
    print(f"  Timeline:   {timeline}")
    
    try:
        if not email_generator_agent:
            print("\n  ❌ ERROR: Email generator agent not available")
            return None
        
        print_section("Generating Email via Gemini AI")
        
        email_result = email_generator_agent.generate_email(
            company=company,
            requirement=requirement,
            budget=budget,
            timeline=timeline,
            priority=priority,
        )
        
        print(f"  ✓ Email generated successfully")
        
        print_section("Generated Email")
        print_email(email_result.subject, email_result.email)
        
        print_section("Tone and Approach")
        guidance = email_generator_agent.get_email_tone_guidance(priority)
        print(f"  {guidance}")
        
        return {
            "company": company,
            "priority": priority,
            "subject": email_result.subject,
            "email": email_result.email,
            "guidance": guidance,
        }
        
    except Exception as e:
        print(f"\n  ❌ ERROR: {str(e)}")
        return None


def batch_generate_emails():
    """Generate emails for multiple leads in batch."""
    print_header("BATCH EMAIL GENERATION - Multiple Leads")
    
    leads = [
        {
            "company": "Enterprise Corp",
            "requirement": "Comprehensive AI strategy for digital transformation",
            "budget": "$500K+",
            "timeline": "Q2 2024",
            "priority": "Hot"
        },
        {
            "company": "MidMarket Services",
            "requirement": "Process automation for back-office operations",
            "budget": "$100K-$150K",
            "timeline": "Q3 2024",
            "priority": "Warm"
        },
        {
            "company": "Startup Labs",
            "requirement": "Low-cost AI tools for product development",
            "budget": "$15K-$25K",
            "timeline": "Unknown",
            "priority": "Cold"
        },
    ]
    
    print(f"  Processing {len(leads)} leads for email generation...\n")
    
    if not email_generator_agent:
        print("  ❌ ERROR: Email generator agent not available")
        return None
    
    results = []
    
    try:
        for i, lead in enumerate(leads, 1):
            print(f"  {i}. Generating email for {lead['company']} ({lead['priority']})...")
            
            email_result = email_generator_agent.generate_email(
                company=lead["company"],
                requirement=lead["requirement"],
                budget=lead["budget"],
                timeline=lead["timeline"],
                priority=lead["priority"],
            )
            
            result = {
                "company": lead["company"],
                "priority": lead["priority"],
                "subject": email_result.subject,
                "email": email_result.email,
            }
            
            results.append(result)
            print(f"     ✓ Subject: {email_result.subject[:60]}...")
        
        # Display summary
        print_section("BATCH GENERATION SUMMARY")
        print(f"  Total emails generated: {len(results)}")
        print(f"  By priority:")
        
        priority_counts = {}
        for result in results:
            priority = result["priority"]
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        for priority, count in sorted(priority_counts.items()):
            symbol = "🔥" if priority == "Hot" else "🔶" if priority == "Warm" else "❄️"
            print(f"    {symbol} {priority}: {count}")
        
        return results
        
    except Exception as e:
        print(f"\n  ❌ ERROR during batch generation: {str(e)}")
        return None


def demonstrate_email_variations():
    """Show how emails vary based on priority."""
    print_header("EMAIL VARIATIONS BY PRIORITY")
    
    print("  The EmailGenerationAgent automatically adjusts the email tone,")
    print("  urgency, and call-to-action based on the lead's priority level:\n")
    
    print("  🔥 HOT (80-100 score):")
    print("     • Tone: Urgent and enthusiastic")
    print("     • Focus: Quick wins and immediate value")
    print("     • CTA: Strong call-to-action with clear next steps")
    print("     • Length: Concise (150-200 words)")
    print("     • Goal: Close the meeting quickly")
    
    print("\n  🔶 WARM (50-79 score):")
    print("     • Tone: Professional and consultative")
    print("     • Focus: Education and building interest")
    print("     • CTA: Gentle invitation to conversation")
    print("     • Length: Moderate (150-250 words)")
    print("     • Goal: Nurture and qualify further")
    
    print("\n  ❄️ COLD (0-49 score):")
    print("     • Tone: Helpful and value-focused")
    print("     • Focus: Providing relevant insights upfront")
    print("     • CTA: Soft, no pressure")
    print("     • Length: Can be slightly longer (200+ words)")
    print("     • Goal: Spark interest and add value")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "EMAIL GENERATION AGENT - COMPLETE EXAMPLES" + " " * 17 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Run demonstrations
    hot_result = generate_hot_lead_email()
    warm_result = generate_warm_lead_email()
    cold_result = generate_cold_lead_email()
    batch_results = batch_generate_emails()
    
    demonstrate_email_variations()
    
    # Final summary
    print_header("SUMMARY")
    print("  ✓ Email Generation Agent: Creates professional personalized emails")
    print("  ✓ Priority-Aware: Tone adapts to lead priority (Hot/Warm/Cold)")
    print("  ✓ Professional Quality: Uses Gemini AI for expert writing")
    print("  ✓ Batch Processing: Handle multiple leads efficiently")
    
    print("\n  Generated Emails:")
    if hot_result:
        print(f"    • Hot lead ({hot_result['company']}): Subject length {len(hot_result['subject'])} chars")
    if warm_result:
        print(f"    • Warm lead ({warm_result['company']}): Subject length {len(warm_result['subject'])} chars")
    if cold_result:
        print(f"    • Cold lead ({cold_result['company']}): Subject length {len(cold_result['subject'])} chars")
    
    print("\n  Use the API endpoints:")
    print("  • POST /api/v1/leads/analyze - Analyze lead data")
    print("  • POST /api/v1/leads/score - Score and prioritize lead")
    print("  • POST /api/v1/leads/generate-email - Generate follow-up email")
    print("\n")


if __name__ == "__main__":
    main()
