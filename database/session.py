from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

from app.settings import get_settings

SETTINGS = get_settings()

engine = create_engine(SETTINGS.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

