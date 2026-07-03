# Graph Report - .  (2026-07-03)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 265 nodes · 488 edges · 33 communities (20 shown, 13 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.56)
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

## God Nodes (most connected - your core abstractions)
1. `GeminiService` - 17 edges
2. `EmailGenerationResult` - 16 edges
3. `EmailGenerationRequest` - 15 edges
4. `LeadAnalysisResult` - 14 edges
5. `TestEmailGenerationValidation` - 14 edges
6. `EmailGenerationOutput` - 13 edges
7. `LeadAnalysisRequest` - 12 edges
8. `LeadScoringAgent` - 11 edges
9. `Lead` - 11 edges
10. `main()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `verify_schemas()` --indirect_call--> `LeadAnalysisResult`  [INFERRED]
  VERIFY.py → backend/schemas/lead_schema.py
- `TestCurlExamples` --uses--> `EmailGenerationRequest`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py
- `TestEmailGenerationErrors` --uses--> `EmailGenerationRequest`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py
- `TestEmailGenerationValidation` --uses--> `EmailGenerationRequest`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py
- `TestCurlExamples` --uses--> `EmailGenerationResult`  [INFERRED]
  test_api_email.py → backend/schemas/lead_schema.py

## Import Cycles
- None detected.

## Communities (33 total, 13 thin omitted)

### Community 0 - "GeminiService"
Cohesion: 0.12
Nodes (13): LeadAnalysisAgent, Any, LeadScoringAgent, Any, LeadAnalysisOutput, LeadAnalysisRequest, LeadAnalysisResult, LeadScoringOutput (+5 more)

### Community 1 - "VERIFY.py"
Cohesion: 0.13
Nodes (25): get_email_generation_prompt(), get_lead_analysis_prompt(), get_lead_scoring_prompt(), Any, validate_and_format_analysis_prompt(), validate_and_format_email_prompt(), main(), print_summary() (+17 more)

### Community 2 - "TestEmailGenerationValidation"
Cohesion: 0.10
Nodes (11): Test POST with company name exceeding max length., Test POST with requirement less than minimum., Test POST with invalid priority value., Test that priority values are case-sensitive., Test input validation for email generation endpoint., Test POST with valid input data., Test POST with missing company field., Test POST with missing requirement field. (+3 more)

### Community 3 - "example_email_generation.py"
Cohesion: 0.21
Nodes (18): batch_generate_emails(), demonstrate_email_variations(), generate_cold_lead_email(), generate_hot_lead_email(), generate_warm_lead_email(), main(), print_email(), print_header() (+10 more)

### Community 4 - "leads.py"
Cohesion: 0.27
Nodes (13): analyze_lead_endpoint(), create_lead(), delete_lead(), generate_email_endpoint(), get_lead(), list_leads(), list_qualified_leads(), save_or_update_lead() (+5 more)

### Community 5 - "main.py"
Cohesion: 0.22
Nodes (8): get_settings(), Settings, get_db(), init_db(), startup_event(), validation_exception_handler(), Request, RequestValidationError

### Community 6 - "example_integrated_workflow.py"
Cohesion: 0.23
Nodes (14): display_email_with_context(), format_lead_data(), main(), print_header(), print_section(), process_lead_batch(), process_single_lead(), Three-Agent Integration Example ================================  Complete de (+6 more)

### Community 7 - "EmailGenerationResult"
Cohesion: 0.31
Nodes (12): EmailGenerationOutput, EmailGenerationRequest, EmailGenerationResult, Email Generation API Tests ===========================  Comprehensive test su, Test email generation with different priority levels., Test output format and structure., Test quality of generated emails., Integration tests for email generation. (+4 more)

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
Cohesion: 0.22
Nodes (5): Test POST with invalid JSON., Test POST with unexpected additional fields., Test handling of special characters in company name., Test handling of unicode characters., TestEmailGenerationErrors

### Community 12 - "EmailGenerationAgent"
Cohesion: 0.29
Nodes (3): EmailGenerationAgent, Any, Placeholder for future industry specific customization.

### Community 13 - "example_lead_analysis.py"
Cohesion: 0.33
Nodes (5): example_batch_analysis(), example_lead_analysis(), Example script demonstrating lead analysis functionality.  This script shows h, Demonstrate batch analysis of multiple leads., Demonstrate lead analysis with a sample lead.

### Community 14 - "TestCurlExamples"
Cohesion: 0.47
Nodes (3): Documentation for curl command examples., Example: Generate email for Hot lead.                  curl -X POST "http://lo, TestCurlExamples

## Knowledge Gaps
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EmailGenerationResult` connect `EmailGenerationResult` to `GeminiService`, `TestEmailGenerationValidation`, `leads.py`, `TestEmailGenerationErrors`, `EmailGenerationAgent`, `TestCurlExamples`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `TestEmailGenerationValidation` connect `TestEmailGenerationValidation` to `EmailGenerationResult`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `LeadAnalysisRequest` connect `GeminiService` to `example_lead_scoring.py`, `VERIFY.py`, `leads.py`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `GeminiService` (e.g. with `EmailGenerationAgent` and `LeadAnalysisAgent`) actually correct?**
  _`GeminiService` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `EmailGenerationResult` (e.g. with `EmailGenerationAgent` and `TestCurlExamples`) actually correct?**
  _`EmailGenerationResult` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `EmailGenerationRequest` (e.g. with `TestCurlExamples` and `TestEmailContentQuality`) actually correct?**
  _`EmailGenerationRequest` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `LeadAnalysisResult` (e.g. with `LeadAnalysisAgent` and `LeadScoringAgent`) actually correct?**
  _`LeadAnalysisResult` has 3 INFERRED edges - model-reasoned connections that need verification._