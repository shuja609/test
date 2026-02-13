# app/models/system.py
from typing import Optional
from sqlmodel import Field, SQLModel, table
import logging
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException

from app.core.database import get_session

logging.basicConfig(level=logging.INFO)

class System(SQLModel, table=True):
    """
    System model.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    version: str
    lastUpdated: datetime

class SystemError(Exception):
    """Custom exception for system errors."""
    pass

class SystemBase(SQLModel):
    version: str
    lastUpdated: datetime

class SystemCreate(SystemBase):
    """
    System create model.
    """
    version: str
    lastUpdated: datetime

class SystemUpdate(SystemBase):
    """
    System update model.
    """
    version: str
    lastUpdated: datetime

class SystemRead(SystemBase):
    """
    System read model.
    """
    id: int

def create_system(db: Session, system: SystemSave):
    """
    Create a new system.

    Args:
    - db: The database session.
    - system (SystemSave): The system to be created.

    Returns:
    - The created system.

    Raises:
    - IntegrityError: If the system already exists.
    - HTTPException: If the system failed to create.
    """
    try:
        db_system = System.get_or_create(db, id=None, defaults=system.dict(exclude_unset=True))
        if db_system:
            return db_system
        else:
            raise SystemError("Failed to create system")
    except IntegrityError:
        raise HTTPException(status_code=400, detail="System already exists")
    except Exception as e:
        logging.error(str(e))
        raise SystemError("Failed to create system")

def update_system(db: Session, system_id: int, system: SystemUpdate):
    """
    Update an existing system.

    Args:
    - db: The database session.
    - system_id (int): The ID of the system to be updated.
    - system (SystemUpdate): The updated system.

    Returns:
    - The updated system.

    Raises:
    - HTTPException: If the system failed to update.
    """
    try:
        db_system = db.query(System).filter(System.id == system_id).first()
        if db_system:
            system_data = system.dict(exclude_unset=True)
            for key, value in system_data.items():
                setattr(db_system, key, value)
            db.add(db_system)
            db.commit()
            db.refresh(db_system)
            return db_system
        else:
            raise SystemError("System not found")
    except Exception as e:
        logging.error(str(e))
        raise SystemError("Failed to update system")

def read_system(db: Session, system_id: int):
    """
    Read a system.

    Args:
    - db: The database session.
    - system_id (int): The ID of the system to be read.

    Returns:
    - The system.

    Raises:
    - HTTPException: If the system failed to read.
    """
    try:
        db_system = db.query(System).filter(System.id == system_id).first()
        if db_system:
            return db_system
        else:
            raise SystemError("System not found")
    except Exception as e:
        logging.error(str(e))
        raise SystemError("Failed to read system")

# app/service/system.py
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import EmailError, ValidationError
import logging

from app.core.database import get_session
from app.models.system import System

router = APIRouter()

@router.post("/system", response_model=SystemRead)
def create_system(system: SystemCreate, db: Session = Depends(get_session)):
    """
    Create a new system.

    Args:
    - system (SystemCreate): The system to be created.

    Returns:
    - The created system.

    Raises:
    - HTTPException: If the system failed to create.
    """
    try:
        created_system = System.create(db, obj_in=system)
        return created_system
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=400, detail="Failed to create system")

@router.put("/system/{system_id}", response_model=SystemRead)
def update_system(system_id: int, system: SystemUpdate, db: Session = Depends(get_session)):
    """
    Update an existing system.

    Args:
    - system_id (int): The ID of the system to be updated.
    - system (SystemUpdate): The updated system.

    Returns:
    - The updated system.

    Raises:
    - HTTPException: If the system failed to update.
    """
    try:
        updated_system = update_system(db, system_id, system)
        return updated_system
    except SystemError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/system/{system_id}", response_model=SystemRead)
def read_system(system_id: int, db: Session = Depends(get_session)):
    """
    Read a system.

    Args:
    - system_id (int): The ID of the system to be read.

    Returns:
    - The system.

    Raises:
    - HTTPException: If the system failed to read.
    """
    try:
        read_system = read_system(db, system_id)
        return read_system
    except SystemError as e:
        raise HTTPException(status_code=400, detail=str(e))
