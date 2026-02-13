from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, ValidationError
import logging
from app.models.system import System
from app.models.error import Error

router = APIRouter()


@router.post("/", response_model=System)
async def create_system(
    item: System,
    session: Session = Depends(get_session)
):
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{id}", response_model=System)
async def get_system(
    id: UUID,
    session: Session = Depends(get_session)
):
    item = session.get(System, id)
    if not item:
        raise HTTPException(status_code=404, detail="System not found")
    return item


@router.get("/", response_model=List[System])
async def list_systems(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    try:
        statement = select(System).offset(skip).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{id}", response_model=System)
async def update_system(
    id: UUID,
    item_update: System,
    session: Session = Depends(get_session)
):
    try:
        db_item = session.get(System, id)
        if not db_item:
            raise HTTPException(status_code=404, detail="System not found")
        
        item_data = item_update.model_dump(exclude_unset=True)
        db_item.sqlmodel_update(item_data)
        
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    except ValidationError as e:
        logging.error(str(e))
        invalid_fields = [field.name for field in e.models[0].fields]
        raise HTTPException(status_code=422, detail=f"Invalid fields: {', '.join(invalid_fields)}")
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(System, id)
        if not item:
            raise HTTPException(status_code=404, detail="System not found")
        
        session.delete(item)
        session.commit()
        return
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Duplicate item
@router.post("/duplicate", response_model=None)
async def save_duplicate_system(
    item: System,
    session: Session = Depends(get_session)
):
    try:
        existing_item = session.query(System).filter/System.name == item.name).first()
        if existing_item:
            raise HTTPException(status_code=422, detail="System with same name already exists")
        
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
