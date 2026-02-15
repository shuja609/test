from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """Category model."""
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    parent_id: Optional[UUID] = None
