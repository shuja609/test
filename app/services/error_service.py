from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select
from app.models.error import Error
import logging
from pydantic import ValidationError
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item data")

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
