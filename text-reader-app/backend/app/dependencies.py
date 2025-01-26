from functools import lru_cache
from .database import SessionLocal
from .config import Settings


@lru_cache()
def get_settings():
    return Settings()


def get_db():
    """
    Provides a database session for dependency injection.

    Creates a new database session, yields it for use, and ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
