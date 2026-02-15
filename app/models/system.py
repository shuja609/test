# app/models/system.py
from datetime import datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel
import logging
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)

class System(SQLModel, table=True):
    """System model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    version: str
    lastUpdated: datetime

class SystemBase(SQLModel):
    version: str
    lastUpdated: datetime

class SystemCreate(SystemBase):
    """System create model."""
    pass

# Alias for backward compat
SystemSave = SystemCreate

class SystemUpdate(SystemBase):
    """System update model."""
    pass

class SystemRead(SystemBase):
    """System read model."""
    id: int

class SystemError(Exception):
    """Custom exception for system errors."""
    pass

def create_system(db: Session, system: SystemCreate):
    """Create a new system."""
    try:
        db_system = System(version=system.version, lastUpdated=system.lastUpdated)
        db.add(db_system)
        db.commit()
        db.refresh(db_system)
        return db_system
    except Exception as e:
        logging.error(str(e))
        raise SystemError("Failed to create system")

def update_system(db: Session, system_id: int, system: SystemUpdate):
    """Update an existing system."""
    try:
        db_system = db.get(System, system_id)
        if not db_system:
            raise SystemError("System not found")
        update_data = {k: v for k, v in {"version": system.version, "lastUpdated": system.lastUpdated}.items()}
        for key, value in update_data.items():
            setattr(db_system, key, value)
        db.add(db_system)
        db.commit()
        db.refresh(db_system)
        return db_system
    except Exception as e:
        logging.error(str(e))
        raise SystemError("Failed to update system")

def read_system(db: Session, system_id: int):
    """Read a system."""
    try:
        db_system = db.get(System, system_id)
        if not db_system:
            raise SystemError("System not found")
        return db_system
    except Exception as e:
        logging.error(str(e))
        raise SystemError("Failed to read system")
