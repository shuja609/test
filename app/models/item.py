from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


CATEGORIES = ["Electronics", "Clothing", "Food", "Books", "Other"]


class Item(SQLModel, table=True):
    """Item model."""
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    category: str
    description: Optional[str] = None
    price: Optional[float] = 0.0
    quantity: int = 0
