from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import logging

from app.core.database import get_session
from app.models.item import Item, CATEGORIES
from app.exceptions import InvalidCategoryError, ItemNotFoundError

router = APIRouter()

@router.post("/", response_model=Item)
async def create_item(
    item: Item,
    session: Session = Depends(get_session)
):
    try:
        if item.category not in CATEGORIES:
            raise InvalidCategoryError
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        logging.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Failed to create item")

@router.get("/{id}", response_model=Item)
async def get_item(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(Item, id)
        if not item:
            raise ItemNotFoundError
        return item
    except Exception as e:
        logging.error(f"Error getting item: {e}")
        raise HTTPException(status_code=404, detail="Item not found")

@router.get("/", response_model=List[Item])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    try:
        statement = select(Item).offset(skip).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logging.error(f"Error listing items: {e}")
        raise HTTPException(status_code=500, detail="Failed to list items")

@router.put("/{id}", response_model=Item)
async def update_item(
    id: UUID,
    item_update: Item,
    session: Session = Depends(get_session)
):
    try:
        db_item = session.get(Item, id)
        if not db_item:
            raise ItemNotFoundError
        if item_update.category not in CATEGORIES:
            raise InvalidCategoryError
        item_data = item_update.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(item_data)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    except Exception as e:
        logging.error(f"Error updating item: {e}")
        raise HTTPException(status_code=500, detail="Failed to update item")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(Item, id)
        if not item:
            raise ItemNotFoundError
        session.delete(item)
        session.commit()
    except Exception as e:
        logging.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete item")

@router.get("/summary", response_model=List[Item])
async def get_summary(
    session: Session = Depends(get_session)
):
    try:
        statement = select(Item)
        return session.exec(statement).all()
    except Exception as e:
        logging.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get summary")

@router.get("/categories", response_model=List[str])
async def get_categories():
    try:
        return CATEGORIES
    except Exception as e:
        logging.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get categories")

@router.get("/filter", response_model=List[Item])
async def filter_items(
    name: str = None,
    category: str = None,
    session: Session = Depends(get_session)
):
    try:
        statement = select(Item)
        if name:
            statement = statement.filter(Item.name.like(f"%{name}%"))
        if category:
            statement = statement.filter(Item.category == category)
        return session.exec(statement).all()
    except Exception as e:
        logging.error(f"Error filtering items: {e}")
        raise HTTPException(status_code=500, detail="Failed to filter items")
