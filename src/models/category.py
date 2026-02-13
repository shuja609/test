from typing import Optional
from sqlmodel import Field, SQLModel
import logging
import uuid

# Define categories
CATEGORIES = ["toiletries", "electronics", "clothing"]

class Category(SQLModel, table=True):
    """
    Category model.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True})

    def __init__(self, name: str):
        """
        Initialize the Category model.
        """
        self.name = name

    @classmethod
    def get_categories(cls):
        """
        Get all available categories.
        
        Returns:
        list: List of category names.
        """
        try:
            return CATEGORIES
        except Exception as e:
            logging.error(f"Error getting categories: {e}")
            return []

    @classmethod
    def create_category(cls, name: str):
        """
        Create a new category.
        
        Args:
        name (str): Category name.
        
        Returns:
        Category: The newly created category.
        """
        try:
            category = cls(name=name)
            return category
        except Exception as e:
            logging.error(f"Error creating category: {e}")
            return None

    def __str__(self):
        """
        String representation of the Category model.
        
        Returns:
        str: Category name.
        """
        return self.name

    def __repr__(self):
        """
        Representation of the Category model.
        
        Returns:
        str: Category representation.
        """
        return f"Category(name='{self.name}')"
