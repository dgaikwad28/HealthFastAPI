from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

from app.settings import get_settings

SETTINGS = get_settings()
DATABASE_URL = f"postgresql://{SETTINGS.db_username}:{SETTINGS.db_password}@{SETTINGS.db_host}:{SETTINGS.db_port}/{SETTINGS.db_name}"
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

