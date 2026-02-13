from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.inventory import Inventory
import logging

# Define logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Inventory)
async def create_inventory(
    item: Inventory,
    session: Session = Depends(get_session)
):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        logger.error(f"Error creating inventory: {e}")
        raise HTTPException(status_code=500, detail="Error creating inventory")

@router.get("/{id}", response_model=Inventory)
async def get_inventory(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(Inventory, id)
        if not item:
            raise HTTPException(status_code=404, detail="Inventory not found")
        return item
    except Exception as e:
        logger.error(f"Error getting inventory: {e}")
        raise HTTPException(status_code=500, detail="Error getting inventory")

@router.get("/", response_model=List[Inventory])
async def list_inventorys(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    try:
        statement = select(Inventory).offset(skip).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"Error listing inventory: {e}")
        raise HTTPException(status_code=500, detail="Error listing inventory")

@router.put("/{id}", response_model=Inventory)
async def update_inventory(
    id: UUID,
    item_update: Inventory,
    session: Session = Depends(get_session)
):
    try:
        db_item = session.get(Inventory, id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Inventory not found")
        
        item_data = item_update.model_dict(exclude_unset=True)
        for key, value in item_data.items():
            setattr(db_item, key, value)
        
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    except Exception as e:
        logger.error(f"Error updating inventory: {e}")
        raise HTTPException(status_code=500, detail="Error updating inventory")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(Inventory, id)
        if not item:
            raise HTTPException(status_code=404, detail="Inventory not found")
        
        session.delete(item)
        session.commit()
    except Exception as e:
        logger.error(f"Error deleting inventory: {e}")
        raise HTTPException(status_code=500, detail="Error deleting inventory")

@router.get("/summary", response_model=dict)
async def get_inventory_summary(
    session: Session = Depends(get_session)
):
    try:
        statement = select(Inventory)
        items = session.exec(statement).all()
        total_items = len(items)
        categories = set(item.category for item in items)
        category_count = len(categories)
        
        return {
            "total_items": total_items,
            "category_count": category_count
        }
    except Exception as e:
        logger.error(f"Error getting inventory summary: {e}")
        raise HTTPException(status_code=500, detail="Error getting inventory summary")

@router.get("/category/{category}", response_model=List[Inventory])
async def get_items_by_category(
    category: str,
    session: Session = Depends(get_session)
):
    try:
        statement = select(Inventory).where(Inventory.category == category)
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"Error getting items by category: {e}")
        raise HTTPException(status_code=500, detail="Error getting items by category")

@router.get("/search", response_model=List[Inventory])
async def search_items(
    query: str,
    session: Session = Depends(get_session)
):
    try:
        statement = select(Inventory).where(Inventory.name.contains(query) | Inventory.description.contains(query))
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"Error searching items: {e}")
        raise HTTPException(status_code=500, detail="Error searching items")
