from sqlalchemy import create_engine, StaticPool

from sqlalchemy.orm import sessionmaker

from app.main import app
from database.models import Base
from database.session import get_db

# Setup SQLite database for testing
engine = create_engine(
    "sqlite:///db.sqlite",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)
