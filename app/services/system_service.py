from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select

from app.models.system import System

class SystemService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, item: System) -> System:
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    async def get(self, id: UUID) -> Optional[System]:
        return self.session.get(System, id)

    async def list(self, skip: int = 0, limit: int = 100) -> List[System]:
        statement = select(System).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    async def update(self, id: UUID, update_data: dict) -> Optional[System]:
        db_item = await self.get(id)
        if not db_item:
            return None
            
        for key, value in update_data.items():
            setattr(db_item, key, value)
            
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    async def delete(self, id: UUID) -> bool:
        db_item = await self.get(id)
        if not db_item:
            return False
            
        self.session.delete(db_item)
        self.session.commit()
        return True