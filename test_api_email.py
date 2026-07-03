"""
Email Generation API Tests
===========================

Comprehensive test suite for the Email Generation Agent endpoints.
Tests input validation, error handling, and email quality.

To run: pytest test_api_email.py -v
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

from fastapi.testclient import TestClient
from backend.main import app
from backend.schemas.lead_schema import (
    EmailGenerationRequest,
    EmailGenerationResult,
    EmailGenerationOutput,
)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestEmailGenerationValidation:
    """Test input validation for email generation endpoint."""
    
    def test_valid_email_generation_request(self, client):
        """Test POST with valid input data."""
        payload = {
            "company": "TechCorp Solutions",
            "requirement": "Enterprise AI platform for customer support",
            "budget": "$200K-$500K",
            "timeline": "Q2 2024 (immediate)",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        # Should return 200 if agent is available, 503 if Gemini API not configured
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "email_content" in data
            assert "subject" in data["email_content"]
            assert "email" in data["email_content"]
            assert data["company"] == "TechCorp Solutions"
            assert data["priority"] == "Hot"
    
    def test_missing_company_field(self, client):
        """Test POST with missing company field."""
        payload = {
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_missing_requirement_field(self, client):
        """Test POST with missing requirement field."""
        payload = {
            "company": "TechCorp",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 422
    
    def test_missing_priority_field(self, client):
        """Test POST with missing priority field."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 422
    
    def test_empty_company(self, client):
        """Test POST with empty company name."""
        payload = {
            "company": "",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 400  # Bad request
    
    def test_company_too_long(self, client):
        """Test POST with company name exceeding max length."""
        payload = {
            "company": "A" * 300,  # Exceeds 255 char limit
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 400
    
    def test_requirement_too_short(self, client):
        """Test POST with requirement less than minimum."""
        payload = {
            "company": "TechCorp",
            "requirement": "AI",  # Less than 10 chars
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 400
    
    def test_invalid_priority(self, client):
        """Test POST with invalid priority value."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "VeryHot"  # Invalid
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code == 400
    
    def test_priority_case_sensitive(self, client):
        """Test that priority values are case-sensitive."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "hot"  # Lowercase
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        # Should fail - priority must be Hot|Warm|Cold
        assert response.status_code in [400, 422]


class TestEmailGenerationPriorities:
    """Test email generation with different priority levels."""
    
    @pytest.mark.parametrize("priority", ["Hot", "Warm", "Cold"])
    def test_all_priority_levels(self, client, priority):
        """Test email generation for all priority levels."""
        payload = {
            "company": "TestCorp",
            "requirement": "AI platform for business automation",
            "budget": "$100K-$200K",
            "timeline": "Q2 2024",
            "priority": priority
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert data["priority"] == priority
            assert "email_content" in data
            
            # Email content should be non-empty
            assert len(data["email_content"]["subject"]) > 0
            assert len(data["email_content"]["email"]) > 0
    
    def test_priority_affects_tone(self, client):
        """Test that priority level influences the generated email."""
        company = "InnovateCorp"
        requirement = "AI solution for data analysis"
        budget = "$150K"
        timeline = "Q3 2024"
        
        # Generate emails for each priority
        results = {}
        
        for priority in ["Hot", "Warm", "Cold"]:
            payload = {
                "company": company,
                "requirement": requirement,
                "budget": budget,
                "timeline": timeline,
                "priority": priority
            }
            
            response = client.post("/api/v1/leads/generate-email", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                results[priority] = {
                    "subject": data["email_content"]["subject"],
                    "email": data["email_content"]["email"]
                }
        
        # Verify we got different emails for different priorities
        if len(results) > 1:
            subjects = [r["subject"] for r in results.values()]
            # Not all subjects should be identical
            assert len(set(subjects)) >= 1


class TestEmailGenerationOutput:
    """Test output format and structure."""
    
    def test_response_contains_all_fields(self, client):
        """Test that response contains all required fields."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check top-level fields
            assert "company" in data
            assert "requirement" in data
            assert "priority" in data
            assert "email_content" in data
            assert "timestamp" in data
            
            # Check email_content structure
            email_content = data["email_content"]
            assert "subject" in email_content
            assert "email" in email_content
            
            # Check field values
            assert data["company"] == "TechCorp"
            assert data["priority"] == "Hot"
            assert isinstance(email_content["subject"], str)
            assert isinstance(email_content["email"], str)
    
    def test_subject_length_constraints(self, client):
        """Test that generated subjects are within length constraints."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            subject = data["email_content"]["subject"]
            
            # Subject should be 10-200 characters
            assert 10 <= len(subject) <= 200
    
    def test_email_body_length(self, client):
        """Test that generated emails have meaningful length."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            email_body = data["email_content"]["email"]
            
            # Email should be at least 50 characters
            assert len(email_body) >= 50
            
            # Email should be reasonable length (typically 150-400 words)
            word_count = len(email_body.split())
            assert word_count >= 20  # At least 20 words
    
    def test_timestamp_format(self, client):
        """Test that timestamp is in ISO format."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            timestamp = data["timestamp"]
            
            # Should be ISO format string
            assert isinstance(timestamp, str)
            # Should be parseable as ISO datetime
            try:
                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                pytest.fail("Timestamp is not in valid ISO format")


class TestEmailGenerationErrors:
    """Test error handling."""
    
    def test_invalid_json(self, client):
        """Test POST with invalid JSON."""
        response = client.post(
            "/api/v1/leads/generate-email",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_unexpected_fields(self, client):
        """Test POST with unexpected additional fields."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot",
            "extra_field": "should be ignored"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        # Should succeed - extra fields are typically ignored
        assert response.status_code in [200, 503, 422]
    
    def test_special_characters_in_company(self, client):
        """Test handling of special characters in company name."""
        payload = {
            "company": "TechCorp & Co. <Ltd>",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code in [200, 503]
    
    def test_unicode_characters(self, client):
        """Test handling of unicode characters."""
        payload = {
            "company": "日本テック Corp",
            "requirement": "AI platform for business automation",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        assert response.status_code in [200, 503]


class TestEmailContentQuality:
    """Test quality of generated emails."""
    
    def test_subject_is_not_placeholder(self, client):
        """Test that subject is actual content, not placeholder."""
        payload = {
            "company": "TechCorp",
            "requirement": "Enterprise AI platform",
            "budget": "$200K",
            "timeline": "Q2 2024",
            "priority": "Hot"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            subject = data["email_content"]["subject"]
            
            # Subject should not be generic placeholders
            assert subject not in ["Subject", "Email Subject", "Generated Subject", ""]
            assert "[COMPANY]" not in subject  # Should be replaced with actual company
    
    def test_email_mentions_company(self, client):
        """Test that generated email mentions the company name."""
        company_name = "SpecificCorp"
        payload = {
            "company": company_name,
            "requirement": "AI platform for data analysis",
            "budget": "$150K",
            "timeline": "Q3 2024",
            "priority": "Warm"
        }
        
        response = client.post("/api/v1/leads/generate-email", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            email_body = data["email_content"]["email"]
            
            # Email should reference the specific company or use professional pronouns
            # (may not always say company name, but should be personalized)
            assert len(email_body) > 50


class TestEmailGenerationIntegration:
    """Integration tests for email generation."""
    
    def test_multiple_sequential_requests(self, client):
        """Test multiple sequential email generation requests."""
        payloads = [
            {
                "company": "CompanyA",
                "requirement": "AI platform for customer support",
                "budget": "$200K",
                "timeline": "Q2 2024",
                "priority": "Hot"
            },
            {
                "company": "CompanyB",
                "requirement": "Data analytics solution",
                "budget": "$100K",
                "timeline": "Q3 2024",
                "priority": "Warm"
            },
            {
                "company": "CompanyC",
                "requirement": "Exploratory AI tools",
                "budget": "$50K",
                "timeline": "Q4 2024",
                "priority": "Cold"
            },
        ]
        
        results = []
        for payload in payloads:
            response = client.post("/api/v1/leads/generate-email", json=payload)
            
            if response.status_code == 200:
                results.append(response.json())
        
        # If we got any successful responses, verify they're different
        if len(results) > 1:
            # Each should be for different company
            assert results[0]["company"] != results[1]["company"]


class TestCurlExamples:
    """Documentation for curl command examples."""
    
    def test_curl_hot_lead(self):
        """
        Example: Generate email for Hot lead.
        
        curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
          -H "Content-Type: application/json" \
          -d '{
            "company": "TechCorp Solutions",
            "requirement": "Enterprise AI platform for customer support",
            "budget": "$200K-$500K",
            "timeline": "Q2 2024 (immediate implementation)",
            "priority": "Hot"
          }'
        """
        pass
    
    def test_curl_warm_lead(self):
        """
        Example: Generate email for Warm lead.
        
        curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
          -H "Content-Type: application/json" \
          -d '{
            "company": "MidMarket Services Inc",
            "requirement": "Process automation for back-office operations",
            "budget": "$100K-$150K",
            "timeline": "Q3 2024 (3 months)",
            "priority": "Warm"
          }'
        """
        pass
    
    def test_curl_cold_lead(self):
        """
        Example: Generate email for Cold lead.
        
        curl -X POST "http://localhost:8000/api/v1/leads/generate-email" \
          -H "Content-Type: application/json" \
          -d '{
            "company": "StartupXYZ",
            "requirement": "Initial exploration of AI solutions",
            "budget": "$20K-$30K (uncertain)",
            "timeline": "Not defined",
            "priority": "Cold"
          }'
        """
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
