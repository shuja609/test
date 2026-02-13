from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select, Field

from app.core.database import get_session
from app.models.user import User, UserCreate, UserUpdate
import logging

# Define logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(
    item: UserCreate,
    session: Session = Depends(get_session)
):
    try:
        user = User.create(session, model_create=True, obj_in=item)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.json())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

@router.get("/{id}", response_model=User)
async def get_user(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(User, id)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

@router.get("/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    try:
        statement = select(User).offset(skip).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

@router.put("/{id}", response_model=User)
async def update_user(
    id: UUID,
    item_update: UserUpdate,
    session: Session = Depends(get_session)
):
    try:
        db_item = session.get(User, id)
        if not db_item:
            raise HTTPException(status_code=404, detail="User not found")
        
        item_data = item_update.dict(exclude_unset=True)
        db_item.sqlmodel_update(item_data)
        
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.json())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID,
    session: Session = Depends(get_session)
):
    try:
        item = session.get(User, id)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        
        session.delete(item)
        session.commit()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]

from typing import Any
from fastapi import HTTPException
from sqlmodel import Session

from app.models.user import User

def verify_duplicate_email(session: Session, email: str) -> bool:
    try:
        session.query(User).filter(User.email == email).first()
        return True
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False
