from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select

from app.models.category import Category
import logging

class CategoryService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, item: Category) -> Category:
        try:
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item
        except Exception as e:
            logging.error(f"Failed to create category: {e}")
            raise

    async def get(self, id: UUID) -> Optional[Category]:
        try:
            return self.session.get(Category, id)
        except Exception as e:
            logging.error(f"Failed to retrieve category: {e}")
            raise

    async def list(self, skip: int = 0, limit: int = 100) -> List[Category]:
        try:
            statement = select(Category).offset(skip).limit(limit)
            return self.session.exec(statement).all()
        except Exception as e:
            logging.error(f"Failed to retrieve categories: {e}")
            raise

    async def update(self, id: UUID, update_data: dict) -> Optional[Category]:
        try:
            db_item = await self.get(id)
            if not db_item:
                logging.error("Category not found")
                return None

            for key, value in update_data.items():
                setattr(db_item, key, value)

            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            return db_item
        except Exception as e:
            logging.error(f"Failed to update category: {e}")
            raise

    async def delete(self, id: UUID) -> bool:
        try:
            db_item = await self.get(id)
            if not db_item:
                logging.error("Category not found")
                return False

            self.session.delete(db_item)
            self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to delete category: {e}")
            raise
