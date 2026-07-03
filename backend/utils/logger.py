import logging
import sys
from backend.config.settings import get_settings

settings = get_settings()

logging.basicConfig(
    level=logging.getLevelName(settings.LOG_LEVEL),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app_logger = logging.getLogger("ai_lead")
