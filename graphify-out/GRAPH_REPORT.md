# Graph Report - AI-LEAD  (2026-07-03)

## Corpus Check
- 48 files · ~45,308 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 660 nodes · 900 edges · 49 communities (46 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `037184d4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_GeminiService|GeminiService]]
- [[_COMMUNITY_VERIFY.py|VERIFY.py]]
- [[_COMMUNITY_TestEmailGenerationValidation|TestEmailGenerationValidation]]
- [[_COMMUNITY_example_email_generation.py|example_email_generation.py]]
- [[_COMMUNITY_leads.py|leads.py]]
- [[_COMMUNITY_main.py|main.py]]
- [[_COMMUNITY_example_integrated_workflow.py|example_integrated_workflow.py]]
- [[_COMMUNITY_EmailGenerationResult|EmailGenerationResult]]
- [[_COMMUNITY_example_lead_scoring.py|example_lead_scoring.py]]
- [[_COMMUNITY_test_api.py|test_api.py]]
- [[_COMMUNITY_test_api_scoring.py|test_api_scoring.py]]
- [[_COMMUNITY_TestEmailGenerationErrors|TestEmailGenerationErrors]]
- [[_COMMUNITY_EmailGenerationAgent|EmailGenerationAgent]]
- [[_COMMUNITY_example_lead_analysis.py|example_lead_analysis.py]]
- [[_COMMUNITY_TestCurlExamples|TestCurlExamples]]
- [[_COMMUNITY_QUICK_START.py|QUICK_START.py]]
- [[_COMMUNITY_ARCHITECTURE.py|ARCHITECTURE.py]]
- [[_COMMUNITY_IMPLEMENTATION_SUMMARY.py|IMPLEMENTATION_SUMMARY.py]]
- [[_COMMUNITY_client|client]]
- [[_COMMUNITY_.test_all_priority_levels|.test_all_priority_levels]]
- [[_COMMUNITY_.test_priority_affects_tone|.test_priority_affects_tone]]
- [[_COMMUNITY_.test_response_contains_all_fields|.test_response_contains_all_fields]]
- [[_COMMUNITY_.test_subject_length_constraints|.test_subject_length_constraints]]
- [[_COMMUNITY_.test_email_body_length|.test_email_body_length]]
- [[_COMMUNITY_.test_timestamp_format|.test_timestamp_format]]
- [[_COMMUNITY_.test_subject_is_not_placeholder|.test_subject_is_not_placeholder]]
- [[_COMMUNITY_.test_email_mentions_company|.test_email_mentions_company]]
- [[_COMMUNITY_.test_multiple_sequential_requests|.test_multiple_sequential_requests]]
- [[_COMMUNITY_Key Features|Key Features]]
- [[_COMMUNITY_Implementation Details|Implementation Details]]
- [[_COMMUNITY_❓ Troubleshooting|❓ Troubleshooting]]
- [[_COMMUNITY_💻 Usage Examples|💻 Usage Examples]]
- [[_COMMUNITY_Priority Levels & Email Strategies|Priority Levels & Email Strategies]]
- [[_COMMUNITY_Production Deployment|Production Deployment]]
- [[_COMMUNITY_Testing|Testing]]
- [[_COMMUNITY_Prompt Engineering|Prompt Engineering]]
- [[_COMMUNITY_Performance Considerations|Performance Considerations]]
- [[_COMMUNITY_🚀 Quick Start (5 Minutes)|🚀 Quick Start (5 Minutes)]]
- [[_COMMUNITY_🔥 Priority Levels Explained|🔥 Priority Levels Explained]]
- [[_COMMUNITY_🎯 What This System Does|🎯 What This System Does]]
- [[_COMMUNITY_🧪 Testing|🧪 Testing]]
- [[_COMMUNITY_Architecture|Architecture]]
- [[_COMMUNITY_Integration with Other Agents|Integration with Other Agents]]
- [[_COMMUNITY_📋 Architecture Overview|📋 Architecture Overview]]

## God Nodes (most connected - your core abstractions)
1. `AI Lead Qualification & Follow-up Agent` - 19 edges
2. `Email Generation Agent - Complete Implementation Guide` - 18 edges
3. `EmailGenerationRequest` - 17 edges
4. `GeminiService` - 17 edges
5. `Lead Analysis Agent - Implementation Guide` - 17 edges
6. `EmailGenerationResult` - 16 edges
7. `Email Generation Agent - Comprehensive Documentation` - 16 edges
8. `Lead Scoring Agent - Complete Implementation Guide` - 16 edges
9. `LeadAnalysisResult` - 15 edges
10. `Phase 4 Completion Report - Email Generation Agent` - 15 edges

## Surprising Connections (you probably didn't know these)
- `verify_schemas()` --indirect_call--> `LeadAnalysisResult`  [INFERRED]
  VERIFY.py → backend/schemas/lead_schema.py
- `TestEmailGenerationValidation` --uses--> `EmailGenerationRequest`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py
- `TestEmailGenerationValidation` --uses--> `EmailGenerationResult`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py
- `TestEmailGenerationValidation` --uses--> `EmailGenerationOutput`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py
- `verify_environment()` --calls--> `get_settings()`  [EXTRACTED]
  VERIFY.py → backend/config/settings.py

## Import Cycles
- None detected.

## Communities (49 total, 3 thin omitted)

### Community 0 - "GeminiService"
Cohesion: 0.10
Nodes (15): EmailGenerationAgent, Any, Placeholder for future industry specific customization., LeadAnalysisAgent, Any, LeadScoringAgent, Any, get_email_generation_prompt() (+7 more)

### Community 1 - "VERIFY.py"
Cohesion: 0.14
Nodes (19): main(), print_summary(), VERIFICATION & TESTING CHECKLIST  Use this script to verify all Lead Analysis, Check environment configuration., Check all imports work., Check schema definitions., Check agent functionality., Check prompt generation. (+11 more)

### Community 2 - "TestEmailGenerationValidation"
Cohesion: 0.10
Nodes (11): Test POST with company name exceeding max length., Test POST with requirement less than minimum., Test POST with invalid priority value., Test that priority values are case-sensitive., Test input validation for email generation endpoint., Test POST with valid input data., Test POST with missing company field., Test POST with missing requirement field. (+3 more)

### Community 3 - "example_email_generation.py"
Cohesion: 0.21
Nodes (18): batch_generate_emails(), demonstrate_email_variations(), generate_cold_lead_email(), generate_hot_lead_email(), generate_warm_lead_email(), main(), print_email(), print_header() (+10 more)

### Community 4 - "leads.py"
Cohesion: 0.10
Nodes (28): analyze_lead_endpoint(), create_lead(), delete_lead(), generate_email_endpoint(), get_lead(), list_leads(), list_qualified_leads(), save_or_update_lead() (+20 more)

### Community 5 - "main.py"
Cohesion: 0.04
Nodes (51): =============================================================================, =============================================================================, =============================================================================, =============================================================================, =============================================================================, =============================================================================, =============================================================================, ============================================================================= (+43 more)

### Community 6 - "example_integrated_workflow.py"
Cohesion: 0.23
Nodes (14): display_email_with_context(), format_lead_data(), main(), print_header(), print_section(), process_lead_batch(), process_single_lead(), Three-Agent Integration Example ================================  Complete de (+6 more)

### Community 7 - "EmailGenerationResult"
Cohesion: 0.06
Nodes (37): EmailGenerationOutput, EmailGenerationRequest, EmailGenerationResult, LeadAnalysisOutput, LeadScoringOutput, LeadScoringResult, BaseModel, client() (+29 more)

### Community 8 - "example_lead_scoring.py"
Cohesion: 0.28
Nodes (12): demonstrate_scoring_ranges(), main(), print_header(), print_section(), Lead Scoring Agent - Complete Implementation Example ==========================, Analyze and score multiple leads - batch processing., Print a formatted header., Demonstrate scoring ranges and priority levels. (+4 more)

### Community 9 - "test_api.py"
Cohesion: 0.22
Nodes (9): main(), print_curl_examples(), print_python_examples(), Any, API Testing Script for Lead Analysis Endpoint.  This script provides examples, Print curl command examples., Print Python request examples., Test the lead analysis endpoint.          Args:         lead_data: Dictionary (+1 more)

### Community 10 - "test_api_scoring.py"
Cohesion: 0.29
Nodes (9): main(), Test scoring a lead using previous analysis results., Test analyzing and scoring multiple leads., Test various error scenarios., Test analyzing a single lead., test_analyze_lead(), test_batch_analysis_and_scoring(), test_error_scenarios() (+1 more)

### Community 11 - "TestEmailGenerationErrors"
Cohesion: 0.04
Nodes (47): API Endpoint Reference, Automated Tests, Batch Email Generation, Code Delivery, Code Quality Standards Met, ❄️ Cold Leads (Score 0-49), Conclusion, Core Technologies (+39 more)

### Community 12 - "EmailGenerationAgent"
Cohesion: 0.04
Nodes (42): 1. Clone or Download the Project, 2. Create Virtual Environment, 3. Install Dependencies, 4. Configure Environment Variables, 5. Initialize Database, 6. Run the Application, 🤖 AI Features (Ready for Implementation), AI Lead Qualification & Follow-up Agent (+34 more)

### Community 13 - "example_lead_analysis.py"
Cohesion: 0.33
Nodes (5): example_batch_analysis(), example_lead_analysis(), Example script demonstrating lead analysis functionality.  This script shows h, Demonstrate batch analysis of multiple leads., Demonstrate lead analysis with a sample lead.

### Community 14 - "TestCurlExamples"
Cohesion: 0.05
Nodes (42): Adjusting Scoring Factors, API Endpoints, Architecture, Batch Lead Scoring, Benchmarks, Changing Priority Levels, Common Errors and Solutions, Common Issues (+34 more)

### Community 21 - "client"
Cohesion: 0.05
Nodes (41): 1. Direct Agent Usage, 1. LeadAnalysisAgent (`backend/agents/lead_analyzer.py`), 2. API Request (cURL), 2. GeminiService (`backend/services/gemini_service.py`), 3. Pydantic Schemas, 3. Python Requests, 4. Prompt Engineering, API Endpoint (+33 more)

### Community 22 - ".test_all_priority_levels"
Cohesion: 0.06
Nodes (31): 1. Verify Installation ✅, 2. Configure Environment 🔑, 3. Start the Server 🚀, "400 Bad Request", 4. Test the API 🧪, "503 Service Unavailable", 5-Minute Setup, API Client (Python) (+23 more)

### Community 23 - ".test_priority_affects_tone"
Cohesion: 0.17
Nodes (12): 1. **EmailGenerationAgent Class** ✅, 2. **Email Generation Prompts** ✅, 3. **Pydantic Validation Schemas** ✅, 4. **FastAPI Endpoint** ✅, 5. **Complete Documentation Package** ✅, 6. **Module Registration Updates** ✅, **EMAIL_GENERATION.md** (~400 lines), **example_email_generation.py** (~400 lines) (+4 more)

### Community 24 - ".test_response_contains_all_fields"
Cohesion: 0.20
Nodes (5): badge(), check_server(), AI Lead Qualification & Follow-up Agent Streamlit Web UI — seamless integration, Render a colored priority badge. Safely handles None., Cache the health check for 5 s to avoid hammering the backend on reruns.

### Community 25 - ".test_subject_length_constraints"
Cohesion: 0.20
Nodes (10): 📞 API Reference, Email Generation Agent - Complete Implementation Guide, Endpoint: POST /api/v1/leads/generate-email, ✨ Key Achievements, 🎓 Learning Path, 📝 License & Attribution, 🎯 Next Steps, 🎯 Overview (+2 more)

### Community 26 - ".test_email_body_length"
Cohesion: 0.29
Nodes (7): Common Issues, Debug Logging, Email Generation Agent - Comprehensive Documentation, Future Enhancements, Overview, Support & Questions, Troubleshooting

### Community 27 - ".test_timestamp_format"
Cohesion: 0.33
Nodes (6): 🛠️ Common Tasks, Generate a Hot Lead Email, Generate a Warm Lead Email, Generate Multiple Emails (Batch), Test the Endpoint, View Complete System Workflow

### Community 28 - ".test_subject_is_not_placeholder"
Cohesion: 0.33
Nodes (6): 📚 Documentation Index, For Complete Details, For Getting Started, For Implementation, For Project Overview, For Testing

### Community 29 - ".test_email_mentions_company"
Cohesion: 0.40
Nodes (5): API Endpoint, POST `/api/v1/leads/generate-email`, Request Schema: `EmailGenerationRequest`, Response Schema: `EmailGenerationOutput`, Status Codes

### Community 30 - ".test_multiple_sequential_requests"
Cohesion: 0.40
Nodes (5): Batch Email Generation, FastAPI HTTP Request, Python Client, Python FastAPI Client, Usage Examples

### Community 33 - "Key Features"
Cohesion: 0.40
Nodes (5): ✅ Batch Processing, ✅ Comprehensive Error Handling, Key Features, ✅ Priority-Aware Email Generation, ✅ Professional Quality

### Community 34 - "Implementation Details"
Cohesion: 0.40
Nodes (5): EmailGenerationAgent, Error Handling Strategy, File Structure, Implementation Details, Key Classes

### Community 35 - "❓ Troubleshooting"
Cohesion: 0.40
Nodes (5): API Slow (>10 seconds), Email Looks Generic, Error: "400 Bad Request", Error: "503 Service Unavailable", ❓ Troubleshooting

### Community 36 - "💻 Usage Examples"
Cohesion: 0.40
Nodes (5): HTTP: Simple curl Request, HTTP: Using Python requests, Python: Batch Processing, Python: Simple Email Generation, 💻 Usage Examples

### Community 37 - "Priority Levels & Email Strategies"
Cohesion: 0.50
Nodes (4): ❄️ Cold Leads (Score: 0-49), 🔥 Hot Leads (Score: 80-100), Priority Levels & Email Strategies, 🔶 Warm Leads (Score: 50-79)

### Community 38 - "Production Deployment"
Cohesion: 0.50
Nodes (4): Environment Configuration, Health Check, Monitoring, Production Deployment

### Community 39 - "Testing"
Cohesion: 0.50
Nodes (4): Example Test Runs, Running Tests, Test Categories, Testing

### Community 40 - "Prompt Engineering"
Cohesion: 0.50
Nodes (4): JSON Output Instruction, Prompt Engineering, System Prompt Design, User Prompt Construction

### Community 41 - "Performance Considerations"
Cohesion: 0.50
Nodes (4): Optimization Strategies, Performance Considerations, Scalability, Speed

### Community 42 - "🚀 Quick Start (5 Minutes)"
Cohesion: 0.50
Nodes (4): 1. Set Your API Key, 2. Start the Server, 3. Generate an Email, 🚀 Quick Start (5 Minutes)

### Community 43 - "🔥 Priority Levels Explained"
Cohesion: 0.50
Nodes (4): ❄️ Cold (Score 0-49), 🔥 Hot (Score 80-100), 🔥 Priority Levels Explained, 🔶 Warm (Score 50-79)

### Community 44 - "🎯 What This System Does"
Cohesion: 0.50
Nodes (4): Key Features, Problem Solved, Solution, 🎯 What This System Does

### Community 45 - "🧪 Testing"
Cohesion: 0.50
Nodes (4): Run All Tests, Run Specific Test Category, Run with Coverage, 🧪 Testing

### Community 46 - "Architecture"
Cohesion: 0.67
Nodes (3): Architecture, Component Hierarchy, Data Flow

### Community 47 - "Integration with Other Agents"
Cohesion: 0.67
Nodes (3): Example Multi-Agent Flow, Integration with Other Agents, Three-Agent Workflow

### Community 48 - "📋 Architecture Overview"
Cohesion: 0.67
Nodes (3): 📋 Architecture Overview, Data Flow, Directory Structure

## Knowledge Gaps
- **287 isolated node(s):** `Overview`, `✅ Priority-Aware Email Generation`, `✅ Professional Quality`, `✅ Batch Processing`, `✅ Comprehensive Error Handling` (+282 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Phase 4 Completion Report - Email Generation Agent` connect `TestEmailGenerationErrors` to `.test_all_priority_levels`, `.test_priority_affects_tone`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `Email Generation Agent - Comprehensive Documentation` connect `.test_email_body_length` to `Key Features`, `Implementation Details`, `Priority Levels & Email Strategies`, `Production Deployment`, `Testing`, `Prompt Engineering`, `Performance Considerations`, `Architecture`, `Integration with Other Agents`, `.test_all_priority_levels`, `.test_email_mentions_company`, `.test_multiple_sequential_requests`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `Email Generation Agent - Complete Implementation Guide` connect `.test_subject_length_constraints` to `❓ Troubleshooting`, `💻 Usage Examples`, `🚀 Quick Start (5 Minutes)`, `🔥 Priority Levels Explained`, `🎯 What This System Does`, `🧪 Testing`, `📋 Architecture Overview`, `.test_all_priority_levels`, `.test_timestamp_format`, `.test_subject_is_not_placeholder`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `EmailGenerationRequest` (e.g. with `TestCurlExamples` and `TestEmailContentQuality`) actually correct?**
  _`EmailGenerationRequest` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `GeminiService` (e.g. with `EmailGenerationAgent` and `LeadAnalysisAgent`) actually correct?**
  _`GeminiService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ARCHITECTURE & INTEGRATION DIAGRAM  Visual representation of the Lead Analysis`, `IMPLEMENTATION SUMMARY Lead Analysis Agent with Google Gemini API Integration`, `Quick Start Guide for Lead Analysis Agent  This file provides step-by-step ins` to the rest of the system?**
  _371 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GeminiService` be split into smaller, more focused modules?**
  _Cohesion score 0.10452961672473868 - nodes in this community are weakly interconnected._