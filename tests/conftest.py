import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    """
    Create a fresh in-memory database for each test.
    """
    engine = create_engine(
        "sqlite:///:memory:", # In-memory SQLite
        connect_args={"check_same_thread": False},
        poolclass=StaticPool, # Singleton thread pool for in-memory
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a TestClient that uses the in-memory DB session.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    
    app.dependency_overrides.clear()