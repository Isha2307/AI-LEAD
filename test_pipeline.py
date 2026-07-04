import requests

base_url = "http://127.0.0.1:8000/api/v1/leads"
email_content = """
From: Joe Pozzuoli <joe@joespizzanyc.com>
Date: Sat, Jul 4, 2026 at 11:30 AM
Subject: Question about your software

Hi there,
I own Joe's Pizza in Greenwich Village. We're looking for a simple way to track our daily flour and tomato deliveries because our current spreadsheet isn't cutting it anymore. 
Your website said you do "orchestration" - does that mean you can help us organize our inventory? We don't have a big budget, maybe $50 a month, just need something simple for my manager to use on his iPad.
Let me know if you can help.
Thanks,
Joe
Joe's Pizza NYC
"""

print("1. Analyzing email...")
res1 = requests.post(f"{base_url}/analyze-email", json={"email_content": email_content})
if not res1.ok:
    print("Error:", res1.text)
    exit(1)
data1 = res1.json()
print("Analyze OK:", data1["company"])

print("2. Scoring lead...")
res2 = requests.post(f"{base_url}/score", json={
    "name": data1["name"],
    "email": data1["email"],
    "company": data1["company"],
    "industry": data1["industry"],
    "employee_count": data1["employee_count"],
    "lead_message": data1["lead_message"],
    "analysis": data1["analysis"]
})
if not res2.ok:
    print("Error:", res2.text)
    exit(1)
data2 = res2.json()
print("Score OK:", data2["scoring"]["priority"])

print("3. Generating email...")
res3 = requests.post(f"{base_url}/generate-email", json={
    "company": data1["company"],
    "requirement": data1["lead_message"],
    "budget": "Unknown",
    "timeline": "As soon as possible",
    "priority": data2["scoring"]["priority"]
})
if not res3.ok:
    print("Error:", res3.text)
    exit(1)
data3 = res3.json()
print("Generate OK:", data3["email_content"]["subject"])

print("ALL PASSED!")
