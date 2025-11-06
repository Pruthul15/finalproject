# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the default engine and sessionmaker
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine(database_url: str = SQLALCHEMY_DATABASE_URL):
    """Factory function to create a new SQLAlchemy engine."""
    if "sqlite" in database_url:
        return create_engine(database_url, connect_args={"check_same_thread": False})
    return create_engine(database_url)

def get_sessionmaker(engine):
    """Factory function to create a new sessionmaker bound to the given engine."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)