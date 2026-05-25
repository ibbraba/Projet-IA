from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


def get_engine():
	settings = get_settings()
	return create_engine(settings.database_url) if settings.database_url else None


def get_session_factory():
	engine = get_engine()
	if engine is None:
		return None
	return sessionmaker(autocommit=False, autoflush=False, bind=engine)
