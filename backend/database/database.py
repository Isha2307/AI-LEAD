from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config.settings import get_settings
from pymongo import MongoClient
import urllib.parse

settings = get_settings()

Base = declarative_base()

mongo_client = None
engine = None

if settings.IS_MONGODB:
    mongo_client = MongoClient(settings.DATABASE_URL)


else:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    if settings.IS_MONGODB:
        # Verify connection and ensure indexes
        db = get_mongodb_client_db()
        # Create an index on email for the leads collection
        db.leads.create_index("email", unique=True)
    else:
        if Base is not None and engine is not None:
            Base.metadata.create_all(bind=engine)

def get_mongodb_client_db():
    # Parse DB name from URL or default to 'ai_lead_data'
    parsed = urllib.parse.urlparse(settings.DATABASE_URL)
    db_name = parsed.path.strip("/")
    if not db_name:
        db_name = "ai_lead_data"
    return mongo_client[db_name]

def get_db():
    if settings.IS_MONGODB:
        db = get_mongodb_client_db()
        yield db
    else:
        if SessionLocal is not None:
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()

