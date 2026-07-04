import os
import json
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Load environment variables from .env if present
        load_dotenv()
        
        self.APP_NAME = os.getenv("APP_NAME", "AI Lead Qualification & Follow-up Agent")
        self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
        
        debug_val = os.getenv("DEBUG", "False").lower()
        self.DEBUG = debug_val in ("true", "1", "t", "yes", "y")
        
        reload_val = os.getenv("RELOAD", "False").lower()
        self.RELOAD = reload_val in ("true", "1", "t", "yes", "y")

        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_lead.db")
        self.IS_MONGODB = self.DATABASE_URL.startswith("mongodb://") or self.DATABASE_URL.startswith("mongodb+srv://")

        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

        cors_origins_raw = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:8501"]')
        try:
            self.CORS_ORIGINS = json.loads(cors_origins_raw)
        except Exception:
            self.CORS_ORIGINS = [i.strip() for i in cors_origins_raw.split(",") if i.strip()]

        self.CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True").lower() in ("true", "1", "t", "yes", "y")
        self.CORS_ALLOW_METHODS = ["*"]
        self.CORS_ALLOW_HEADERS = ["*"]

        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        self.STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
        self.STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")

# Singleton settings instance
_settings = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
