"""Database connection and session management."""

from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

from src.config import settings

# Database base class
Base = declarative_base()

# Global engine and session factory
_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None


def get_engine() -> Engine:
    """Get or create database engine.
    
    Returns:
        SQLAlchemy engine instance
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            echo=settings.ENVIRONMENT == "development",
        )
    return _engine


def get_session_factory() -> sessionmaker:
    """Get or create session factory.
    
    Returns:
        SQLAlchemy sessionmaker
    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )
    return _SessionLocal


@contextmanager
def get_db_session():
    """Get a database session with automatic cleanup.
    
    Usage:
        with get_db_session() as session:
            # Use session here
            pass
    """
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


def close_db():
    """Close database connections."""
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None

