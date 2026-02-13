from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.error import Error

router = APIRouter()

@router.post("/", response_model=Error)
async def create_error(
    item: Error,
    session: Session = Depends(get_session)
):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/{id}", response_model=Error)
async def get_error(
    id: UUID,
    session: Session = Depends(get_session)
):
    item = session.get(Error, id)
    if not item:
        raise HTTPException(status_code=404, detail="Error not found")
    return item

@router.get("/", response_model=List[Error])
async def list_errors(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    statement = select(Error).offset(skip).limit(limit)
    return session.exec(statement).all()

@router.put("/{id}", response_model=Error)
async def update_error(
    id: UUID,
    item_update: Error,
    session: Session = Depends(get_session)
):
    db_item = session.get(Error, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Error not found")
    
    item_data = item_update.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_error(
    id: UUID,
    session: Session = Depends(get_session)
):
    item = session.get(Error, id)
    if not item:
        raise HTTPException(status_code=404, detail="Error not found")
    
    session.delete(item)
    session.commit()