from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class Inventory(SQLModel, table=True):
    """Inventory model."""
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    category: str
    description: Optional[str] = None
    quantity: int = 0
