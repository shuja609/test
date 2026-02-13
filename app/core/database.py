from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from app.core import config

# Database URL from settings
database_url = str(config.settings.DATABASE_URL)

connect_args = {"check_same_thread": False} if "sqlite" in database_url else {}
engine = create_engine(database_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session