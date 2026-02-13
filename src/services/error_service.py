from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select
from app.models.error import Error
import logging
from pydantic import ValidationError, EmailError
from fastapi import HTTPException, status

from app.core.database import get_session

# Define logging configuration
logging.basicConfig(level=logging.INFO)

class ErrorService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, item: Error) -> Error:
        try:
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item
        except Exception as e:
            logging.error(f"Error creating item: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating item")

    async def get(self, id: UUID) -> Optional[Error]:
        try:
            return self.session.get(Error, id)
        except Exception as e:
            logging.error(f"Error getting item: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error getting item")

    async def list(self, skip: int = 0, limit: int = 100) -> List[Error]:
        try:
            statement = select(Error).offset(skip).limit(limit)
            return self.session.exec(statement).all()
        except Exception as e:
            logging.error(f"Error listing items: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error listing items")

    async def update(self, id: UUID, update_data: dict) -> Optional[Error]:
        try:
            db_item = await self.get(id)
            if not db_item:
                return None

            for key, value in update_data.items():
                setattr(db_item, key, value)

            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            return db_item
        except Exception as e:
            logging.error(f"Error updating item: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating item")

    async def delete(self, id: UUID) -> bool:
        try:
            db_item = await self.get(id)
            if not db_item:
                return False

            self.session.delete(db_item)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting item: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting item")

    async def validate_item(self, item: Error) -> Error:
        try:
            item.validate()
            return item
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item data", errors=e.errors())

    async def validate_unique_item(self, name: str, category: str) -> bool:
        try:
            db_item = self.session.execute(select(Error).where(Error.name == name)).first()
            if db_item:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with name already exists")

            db_category = self.session.execute(select(Error).where(Error.category == category)).first()
            if db_category:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with category already exists")

            return True
        except Exception as e:
            logging.error(f"Error validating unique item: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error validating unique item")

    async def handle_system_error(self) -> None:
        try:
            raise Exception("System error")
        except Exception as e:
            logging.error(f"System error: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="System error")

# app/models/error.py

from typing import Optional
from sqlmodel import Field, SQLModel, table
import logging
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException
from app.core.database import get_session

# Define logging configuration
logging.basicConfig(level=logging.INFO)

class Error(SQLModel, table):
    id: UUID = Field(default_field=SQLModel.UUID(primary_key=True))
    name: str
    category: str
    description: str
    quantity: int

# app/core/database.py

from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLAlchemy
from app.models.error import Error

ENGINE = None
SESSION_LOCAL = None
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

def get_session() -> Session:
    try:
        global ENGINE
        if ENGINE == None:
            ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
            global SESSION_LOCAL
            SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

        db = SESSION_LOCAL()
        try:
            yield db
        except Exception as e:
            db.rollback()
            logging.error(f"Error getting session: {e}")
            raise
        finally:
            db.close()
    except Exception as e:
        logging.error(f"Error getting session: {e}")
        raise

# tests/test_error_service.py

def test_create_item(tmp_path):
    from app.core.database import db
    from app.models.error import Error

    db.query(Error).delete()
    db.commit()

    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    error_service = ErrorService(db)
    created_item = error_service.create(item)
    assert item.id == created_item.id
    assert item.name == created_item.name
    assert item.category == created_item.category
    assert item.description == created_item.description
    assert item.quantity == created_item.quantity

def test_get_item(tmp_path):
    from app.core.database import db
    from app.models.error import Error

    db.query(Error).delete()
    db.commit()

    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    error_service = ErrorService(db)
    created_item = error_service.create(item)

    fetched_item = error_service.get(created_item.id)
    assert fetched_item.id == created_item.id
    assert fetched_item.name == created_item.name
    assert fetched_item.category == created_item.category
    assert fetched_item.description == created_item.description
    assert fetched_item.quantity == created_item.quantity

def test_list_items(tmp_path):
    from app.core.database import db
    from app.models.error import Error

    db.query(Error).delete()
    db.commit()

    item1 = Error(name="Test Item 1", category="Test Category", description="Test Description", quantity=10)
    item2 = Error(name="Test Item 2", category="Test Category", description="Test Description", quantity=20)
    error_service = ErrorService(db)

    error_service.create(item1)
    error_service.create(item2)

    items = error_service.list()
    assert len(items) == 2
    assert items[0].id == item1.id
    assert items[0].name == item1.name
    assert items[0].category == item1.category
    assert items[0].description == item1.description
    assert items[0].quantity == item1.quantity
    assert items[1].id == item2.id
    assert items[1].name == item2.name
    assert items[1].category == item2.category
    assert items[1].description == item2.description
    assert items[1].quantity == item2.quantity

def test_update_item(tmp_path):
    from app.core.database import db
    from app.models.error import Error

    db.query(Error).delete()
    db.commit()

    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    error_service = ErrorService(db)
    created_item = error_service.create(item)

    updated_item = error_service.update(created_item.id, {"name": "Updated Test Item", "category": "Updated Test Category"})
    assert updated_item.id == created_item.id
    assert updated_item.name == "Updated Test Item"
    assert updated_item.category == "Updated Test Category"
    assert updated_item.description == created_item.description
    assert updated_item.quantity == created_item.quantity

def test_delete_item(tmp_path):
    from app.core.database import db
    from app.models.error import Error

    db.query(Error).delete()
    db.commit()

    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    error_service = ErrorService(db)
    created_item = error_service.create(item)

    success = error_service.delete(created_item.id)
    assert success
    with pytest.raises(HTTPException) as exc:
        error_service.get(created_item.id)
    assert exc.value.status_code == 404
