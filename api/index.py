"""
Vercel serverless entry point for the FastAPI backend.
Vercel imports this file and uses the `app` object.
"""
import sys
import os

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app  # noqa: F401 — Vercel needs this exported as `app`
