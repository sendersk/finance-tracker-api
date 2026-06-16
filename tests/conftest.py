import pytest
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.database import Base

TEST_DATABASE_URL = "sqlite:///test_finance.db"

engine = create_engine(
    TEST_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def db_session() -> Generator[Session]:
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

    Base.metadata.drop_all(bind=engine)