"""
ARCHITECTURE & INTEGRATION DIAGRAM

Visual representation of the Lead Analysis Agent implementation
"""

SYSTEM_ARCHITECTURE = r"""
┌─────────────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATION                              │
│                  (FastAPI Frontend, Streamlit, etc.)                     │
└────────────────────────┬────────────────────────────────────────────────┘
                         │
                         │ POST /api/v1/leads/analyze
                         │ {name, email, company, industry, ...}
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                                  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Route Handler: POST /leads/analyze                              │  │
│  │  - Input: LeadAnalysisRequest (Pydantic)                         │  │
│  │  - Validates all fields                                          │  │
│  │  - Calls LeadAnalysisAgent                                       │  │
│  │  - Outputs: LeadAnalysisOutput (JSON)                            │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                         │                                                │
│                         ▼                                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │        LEAD ANALYSIS AGENT (backend/agents/)                    │  │
│  │                                                                   │  │
│  │  analyze_lead()                                                  │  │
│  │  ├─ Input validation                                             │  │
│  │  ├─ Prompt generation                                            │  │
│  │  ├─ Gemini API call                                              │  │
│  │  ├─ JSON extraction                                              │  │
│  │  ├─ Pydantic validation                                          │  │
│  │  └─ Returns: LeadAnalysisResult                                  │  │
│  │                                                                   │  │
│  │  get_qualification_score()                                       │  │
│  │  └─ Multi-factor scoring algorithm                               │  │
│  │     (Budget, Timeline, Urgency, Pain Points)                     │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                         │                                                │
│                         ▼                                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │     GEMINI SERVICE (backend/services/)                           │  │
│  │                                                                   │  │
│  │  analyze_lead()                                                  │  │
│  │  ├─ Receives lead data & prompts                                 │  │
│  │  ├─ Calls google.generativeai API                                │  │
│  │  ├─ Handles API errors                                           │  │
│  │  └─ Returns: Raw API response                                    │  │
│  │                                                                   │  │
│  │  extract_json_from_text()                                        │  │
│  │  ├─ Attempts multiple JSON extraction methods                    │  │
│  │  ├─ Handles markdown code blocks                                 │  │
│  │  └─ Returns: Parsed JSON dictionary                              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                         │                                                │
└─────────────────────────┼────────────────────────────────────────────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  GOOGLE GEMINI API       │  │  PROMPT TEMPLATES        │
│                          │  │  (backend/prompts/)      │
│ - Model: gemini-pro      │  │                          │
│ - Authentication        │  │  • Lead analysis prompt  │
│ - Rate limiting         │  │  • Follow-up prompt      │
│ - Cost tracking         │  │  • System prompts        │
└──────────────────────────┘  └──────────────────────────┘
             │
             ▼
      ┌─────────────┐
      │ AI Analysis │
      │   Results   │
      └─────────────┘
             │
             ▼
        Base Response:
        {
          "summary": "...",
          "requirement": "...",
          "budget": "...",
          "timeline": "...",
          "urgency": "...",
          "company_size": "...",
          "industry": "...",
          "pain_points": [...]
        }
"""


DATA_FLOW = r"""
INPUT DATA
   │
   ▼
┌─────────────────────────────────────────┐
│   LeadAnalysisRequest (Validation)      │
│  • name (str, 1-255 chars)              │
│  • email (EmailStr)                     │
│  • company (str, 1-255 chars)           │
│  • industry (str, 1-100 chars)          │
│  • employee_count (int >= 1)            │
│  • lead_message (str, >= 10 chars)      │
└─────────────────────┬───────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  Prompt Generation     │
         │  (with lead context)   │
         └────────┬───────────────┘
                  │
                  ▼
        ┌──────────────────────┐
        │  Gemini API Call     │
        │  (analyze_lead())    │
        └────────┬─────────────┘
                 │
                 ▼
      ┌────────────────────────────┐
      │  Gemini Response (Text)    │
      │  (JSON format requested)   │
      └────────┬───────────────────┘
               │
               ▼
      ┌────────────────────────────────┐
      │  JSON Extraction               │
      │  • Direct parsing              │
      │  • Markdown extraction         │
      │  • Object detection            │
      └────────┬───────────────────────┘
               │
               ▼
       ┌──────────────────────────┐
       │   Parsed JSON Dictionary │
       └────────┬─────────────────┘
                │
                ▼
    ┌─────────────────────────────────┐
    │  Pydantic Validation            │
    │  LeadAnalysisResult Schema      │
    │  ✓ All fields present           │
    │  ✓ Correct types                │
    │  ✓ Valid values                 │
    └────────┬────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │  Scoring Algorithm              │
    │  • Budget: 0-25 points          │
    │  • Timeline: 0-25 points        │
    │  • Urgency: 0-25 points         │
    │  • Pain Points: 0-20 points     │
    │  • Total: 0-100                 │
    │  • is_qualified: score >= 60    │
    └────────┬────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │  LeadAnalysisOutput             │
    │  • Lead info                    │
    │  • Analysis results             │
    │  • Timestamp                    │
    └────────┬────────────────────────┘
             │
             ▼
       ┌──────────────────┐
       │  HTTP 200 OK     │
       │  JSON Response   │
       └──────────────────┘
"""


ERROR_HANDLING = r"""
┌─────────────────────────────────────────────────────────┐
│           ERROR HANDLING FLOW                           │
└─────────────────────────────────────────────────────────┘

                        INPUT
                          │
                          ▼
            ┌──────────────────────────┐
            │  Validation Error?       │
            └──────────┬───────────────┘
                 YES   │
                       ▼
              HTTP 400 Bad Request
              "Invalid input: ..."
                       
            NO │
               ▼
            ┌──────────────────────────┐
            │  Gemini API Available?   │
            └──────────┬───────────────┘
                 NO    │
                       ▼
              HTTP 503 Service Unavailable
              "AI service temporarily..."
                       
            YES │
                ▼
            ┌──────────────────────────┐
            │  Valid JSON Response?    │
            └──────────┬───────────────┘
                 NO    │
                       ▼
              HTTP 500 Internal Error
              "Error during analysis"
                       
            YES │
                ▼
            ┌──────────────────────────┐
            │  Schema Validation OK?   │
            └──────────┬───────────────┘
                 NO    │
                       ▼
              HTTP 400 Bad Request
              "Invalid response format"
                       
            YES │
                ▼
              HTTP 200 OK
              Complete Analysis JSON
"""


COMPONENT_RELATIONSHIPS = r"""
┌──────────────────────────────────────────────────────────────┐
│           COMPONENT RELATIONSHIPS                            │
└──────────────────────────────────────────────────────────────┘

API Route (leads.py)
    │
    ├─── LeadAnalysisAgent (lead_analyzer.py)
    │         │
    │         ├─── GeminiService (gemini_service.py)
    │         │         │
    │         │         └─── google.generativeai
    │         │
    │         ├─── Prompts (lead_prompts.py)
    │         │
    │         └─── Logging (logger.py)
    │
    ├─── Schemas (lead_schema.py)
    │         │
    │         ├─── LeadAnalysisRequest (Input)
    │         ├─── LeadAnalysisResult (Analysis)
    │         └─── LeadAnalysisOutput (Response)
    │
    └─── Database (optional storage)
         │
         └─── Lead Model


Configuration:
    │
    ├─── Settings (config/settings.py)
    │         │
    │         └─── GEMINI_API_KEY
    │         └─── GEMINI_MODEL
    │         └─── LOG_LEVEL
    │
    └─── Environment (.env file)
         │
         ├─── GEMINI_API_KEY=sk-proj-xxxxx
         ├─── DATABASE_URL=sqlite:///./ai_lead.db
         └─── DEBUG=False


Dependencies:
    │
    ├─── FastAPI (Web framework)
    ├─── Pydantic (Validation)
    ├─── google-generativeai (Gemini API)
    └─── SQLAlchemy (Database ORM)
"""


COMPLETE_WORKFLOW = r"""
┌──────────────────────────────────────────────────────────────┐
│         COMPLETE LEAD ANALYSIS WORKFLOW                      │
└──────────────────────────────────────────────────────────────┘

STEP 1: REQUEST ARRIVES
═════════════════════════════════════════════════════════════════
   POST /api/v1/leads/analyze
   {
     "name": "John Smith",
     "email": "john@company.com",
     "company": "TechCorp",
     "industry": "Software",
     "employee_count": 500,
     "lead_message": "Looking for AI lead qualification solution"
   }


STEP 2: FASTAPI ROUTE HANDLER
═════════════════════════════════════════════════════════════════
   ✓ Receives request
   ✓ Pydantic validates LeadAnalysisRequest
   ✓ Stores in memory
   ✓ Calls lead_analyzer_agent.analyze_lead()


STEP 3: AGENT ANALYSIS
═════════════════════════════════════════════════════════════════
   ✓ Validates all 6 input fields
   ✓ Generates system prompt (analyst context)
   ✓ Generates user prompt (specific analysis request)
   ✓ Creates GeminiService message payload


STEP 4: GEMINI API CALL
═════════════════════════════════════════════════════════════════
   ✓ GeminiService connects to Google
   ✓ Sends both system & user prompts
   ✓ Instructs: "Return ONLY valid JSON"
   ✓ Waits for response (2-5 seconds typical)


STEP 5: RESPONSE PROCESSING
═════════════════════════════════════════════════════════════════
   ✓ Receives response text from Gemini
   ✓ Attempts 3 JSON extraction methods:
      1. Direct JSON.parse()
      2. Extract from markdown code blocks
      3. Find JSON object in text
   ✓ Extracts clean JSON dictionary


STEP 6: VALIDATION
═════════════════════════════════════════════════════════════════
   ✓ Pydantic validates against LeadAnalysisResult schema
   ✓ Ensures all 8 fields present:
      • summary
      • requirement
      • budget
      • timeline
      • urgency
      • company_size
      • industry
      • pain_points
   ✓ Raises error if validation fails


STEP 7: SCORING
═════════════════════════════════════════════════════════════════
   ✓ Analyzes budget field → 0-25 points
   ✓ Analyzes timeline field → 0-25 points
   ✓ Analyzes urgency field → 0-25 points
   ✓ Counts pain_points → 0-20 points
   ✓ Calculates total score (0-100)
   ✓ Determines: is_qualified = (score >= 60)


STEP 8: RESPONSE FORMATTING
═════════════════════════════════════════════════════════════════
   ✓ Creates LeadAnalysisOutput
   ✓ Includes:
      • Lead name & email
      • Company name
      • Complete analysis
      • Timestamp
   ✓ Serializes to JSON


STEP 9: RESPONSE SENT
═════════════════════════════════════════════════════════════════
   HTTP 200 OK
   Content-Type: application/json
   
   {
     "name": "John Smith",
     "email": "john@company.com",
     "company": "TechCorp",
     "analysis": {
       "summary": "Mid-market SaaS adopting AI...",
       "requirement": "Automated lead qualification...",
       "budget": "$50K-$100K",
       "timeline": "Q2 2024",
       "urgency": "High",
       "company_size": "Mid-Market",
       "industry": "Software",
       "pain_points": [
         "Manual review consuming 30+ hours/week",
         "Inconsistent qualification",
         "Slow response to leads"
       ]
     },
     "timestamp": "2024-01-15T10:30:45.123456"
   }


ERROR SCENARIOS
═════════════════════════════════════════════════════════════════
   Missing Field → HTTP 400
   Invalid Email → HTTP 400
   API Unavailable → HTTP 503
   Invalid JSON → HTTP 500
   Schema Error → HTTP 400
"""


if __name__ == "__main__":
    print("\n" + "="*70)
    print("LEAD ANALYSIS AGENT - ARCHITECTURE & INTEGRATION")
    print("="*70 + "\n")
    
    print(SYSTEM_ARCHITECTURE)
    print("\n" + "="*70)
    print("DATA FLOW")
    print("="*70 + "\n")
    print(DATA_FLOW)
    
    print("\n" + "="*70)
    print("ERROR HANDLING")
    print("="*70 + "\n")
    print(ERROR_HANDLING)
    
    print("\n" + "="*70)
    print("COMPONENT RELATIONSHIPS")
    print("="*70 + "\n")
    print(COMPONENT_RELATIONSHIPS)
    
    print("\n" + "="*70)
    print("COMPLETE WORKFLOW")
    print("="*70 + "\n")
    print(COMPLETE_WORKFLOW)
    
    print("="*70 + "\n")
