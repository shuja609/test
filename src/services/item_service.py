from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select

from app.models.item import Item, CATEGORIES
from app.exceptions import InvalidCategoryError, ItemNotFoundError

class ItemService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, item: Item) -> Item:
        try:
            if item.category not in CATEGORIES:
                raise InvalidCategoryError("Invalid category")
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item
        except Exception as e:
            self.session.rollback()
            raise e

    async def get(self, id: UUID) -> Optional[Item]:
        try:
            return self.session.get(Item, id)
        except Exception as e:
            raise e

    async def list(self, skip: int = 0, limit: int = 100) -> List[Item]:
        try:
            statement = select(Item).offset(skip).limit(limit)
            return self.session.exec(statement).all()
        except Exception as e:
            raise e

    async def update(self, id: UUID, update_data: dict) -> Optional[Item]:
        try:
            db_item = await self.get(id)
            if not db_item:
                raise ItemNotFoundError("Item not found")

            for key, value in update_data.items():
                setattr(db_item, key, value)
                if key == "category" and value not in CATEGORIES:
                    raise InvalidCategoryError("Invalid category")

            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            return db_item
        except Exception as e:
            self.session.rollback()
            raise e

    async def delete(self, id: UUID) -> bool:
        try:
            db_item = await self.get(id)
            if not db_item:
                raise ItemNotFoundError("Item not found")

            self.session.delete(db_item)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    async def filter(self, name: Optional[str] = None, category: Optional[str] = None) -> List[Item]:
        try:
            statement = select(Item)
            if name:
                statement = statement.where(Item.name.contains(name))
            if category:
                if category not in CATEGORIES:
                    raise InvalidCategoryError("Invalid category")
                statement = statement.where(Item.category == category)
            return self.session.exec(statement).all()
        except Exception as e:
            raise e

    async def get_categories(self) -> List[str]:
        try:
            return CATEGORIES
        except Exception as e:
            raise e

    async def get_item_summary(self) -> dict:
        try:
            total_items = self.session.query(Item).count()
            categories = {}
            for category in CATEGORIES:
                category_items = self.session.query(Item).filter(Item.category == category).count()
                categories[category] = category_items
            return {"total_items": total_items, "categories": categories}
        except Exception as e:
            raise e
