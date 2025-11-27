"""LangGraph checkpointer configuration for state persistence."""

from typing import Optional
from langgraph.checkpoint.memory import MemorySaver

from src.config import settings


def get_checkpointer():
    """Get the appropriate checkpointer based on configuration.
    
    Returns:
        Checkpointer instance (PostgresSaver, RedisSaver, or MemorySaver)
    """
    # Try PostgreSQL first
    if settings.DATABASE_URL and "postgresql" in settings.DATABASE_URL.lower():
        try:
            from langgraph.checkpoint.postgres import PostgresSaver
            return PostgresSaver.from_conn_string(settings.DATABASE_URL)
        except ImportError:
            # Package not installed, fall through
            pass
        except Exception:
            # Connection failed, fall through
            pass

    # Try Redis
    if settings.REDIS_URL and "redis" in settings.REDIS_URL.lower():
        try:
            from langgraph.checkpoint.redis import RedisSaver
            return RedisSaver.from_conn_string(settings.REDIS_URL)
        except ImportError:
            # Package not installed, fall through
            pass
        except Exception:
            # Connection failed, fall through
            pass

    # Default to in-memory (for development)
    return MemorySaver()

