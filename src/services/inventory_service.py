from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select

from app.models.inventory import Inventory

class InventoryService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, item: Inventory) -> Inventory:
        try:
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item
        except Exception as e:
            self.session.rollback()
            raise e

    async def get(self, id: UUID) -> Optional[Inventory]:
        try:
            return self.session.get(Inventory, id)
        except Exception as e:
            raise e

    async def list(self, skip: int = 0, limit: int = 100) -> List[Inventory]:
        try:
            statement = select(Inventory).offset(skip).limit(limit)
            return self.session.exec(statement).all()
        except Exception as e:
            raise e

    async def update(self, id: UUID, update_data: dict) -> Optional[Inventory]:
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
            self.session.rollback()
            raise e

    async def delete(self, id: UUID) -> bool:
        try:
            db_item = await self.get(id)
            if not db_item:
                return False
                
            self.session.delete(db_item)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    async def search(self, name: Optional[str] = None, category: Optional[str] = None) -> List[Inventory]:
        try:
            statement = select(Inventory)
            if name:
                statement = statement.filter(Inventory.name == name)
            if category:
                statement = statement.filter(Inventory.category == category)
            return self.session.exec(statement).all()
        except Exception as e:
            raise e

    async def get_summary(self) -> dict:
        try:
            total_items = self.session.query(Inventory).count()
            categories = self.session.query(Inventory.category).distinct().all()
            return {
                "total_items": total_items,
                "categories": categories
            }
        except Exception as e:
            raise e

    async def get_items_by_category(self, category: str) -> List[Inventory]:
        try:
            statement = select(Inventory).filter(Inventory.category == category)
            return self.session.exec(statement).all()
        except Exception as e:
            raise e

    async def filter_items(self, name: Optional[str] = None, category: Optional[str] = None) -> List[Inventory]:
        try:
            statement = select(Inventory)
            if name:
                statement = statement.filter(Inventory.name == name)
            if category:
                statement = statement.filter(Inventory.category == category)
            return self.session.exec(statement).all()
        except Exception as e:
            raise e
