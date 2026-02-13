from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.category import Category
import logging

router = APIRouter()

@router.post("/", response_model=Category)
async def create_category(
    item: Category,
    session: Session = Depends(get_session)
):
    try:
        logging.info("Create category request")
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        logging.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create category")

@router.get("/{id}", response_model=Category)
async def get_category(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        logging.info(f"Get category request for id: {id}")
        item = session.get(Category, id)
        if not item:
            raise HTTPException(status_code=404, detail="Category not found")
        return item
    except Exception as e:
        logging.error(f"Error getting category: {e}")
        raise HTTPException(status_code=500, detail="Failed to get category")

@router.get("/", response_model=List[Category])
async def list_categorys(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    try:
        logging.info("List categories request")
        statement = select(Category).offset(skip).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logging.error(f"Error listing categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to list categories")

@router.put("/{id}", response_model=Category)
async def update_category(
    id: UUID,
    item_update: Category,
    session: Session = Depends(get_session)
):
    try:
        logging.info(f"Update category request for id: {id}")
        db_item = session.get(Category, id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Category not found")
        
        item_data = item_update.dict(exclude_unset=True)
        for key, value in item_data.items():
            setattr(db_item, key, value)
        
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    except Exception as e:
        logging.error(f"Error updating category: {e}")
        raise HTTPException(status_code=500, detail="Failed to update category")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        logging.info(f"Delete category request for id: {id}")
        item = session.get(Category, id)
        if not item:
            raise HTTPException(status_code=404, detail="Category not found")
        
        session.delete(item)
        session.commit()
    except Exception as e:
        logging.error(f"Error deleting category: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete category")
