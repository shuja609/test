from typing import List, Optional
from sqlmodel import SQLModel, Field, Session
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class User(SQLModel, table=True):
    """User model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    password: str
    inventory: Optional[str] = None

class UserCreate(SQLModel):
    """User create schema."""
    username: str
    email: str
    password: str
    inventory: Optional[str] = None

class UserUpdate(SQLModel):
    """User update schema."""
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    inventory: Optional[str] = None
