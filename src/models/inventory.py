from typing import List, Optional
from sqlmodel import Field, SQLModel
import logging
import uuid
from sqlmodel import Session, select
from app.models.item import Item
from app.models.category import Category

# Define logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Inventory(SQLModel, table=True):
    """
    Inventory model.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    items: List[Item] = Field(default_factory=list)
    categories: List[Category] = Field(default_factory=list)

    def add_item(self, item: Item, session: Session):
        """
        Add a new item to the inventory.
        """
        try:
            # Check if the item already exists in the inventory
            existing_item = session.exec(select(Item).where(Item.name == item.name)).first()
            if existing_item:
                # Update the quantity of the existing item
                existing_item.quantity += item.quantity
                session.add(existing_item)
                session.commit()
            else:
                # Add the new item to the inventory
                self.items.append(item)
                session.add(self)
                session.commit()
        except Exception as e:
            logger.error(f"Error adding item to inventory: {e}")
            raise

    def update_item(self, item_id: str, quantity: int, description: str, session: Session):
        """
        Update an existing item in the inventory.
        """
        try:
            # Find the item to update
            item_to_update = next((item for item in self.items if item.id == item_id), None)
            if item_to_update:
                # Update the item's quantity and description
                item_to_update.quantity = quantity
                item_to_update.description = description
                session.add(item_to_update)
                session.commit()
            else:
                logger.error(f"Item not found in inventory: {item_id}")
                raise ItemNotFoundError
        except Exception as e:
            logger.error(f"Error updating item in inventory: {e}")
            raise

    def retrieve_item(self, item_name: str, session: Session):
        """
        Retrieve an item from the inventory by name.
        """
        try:
            # Find the item by name
            item = next((item for item in self.items if item.name == item_name), None)
            if item:
                return item
            else:
                logger.error(f"Item not found in inventory: {item_name}")
                raise ItemNotFoundError
        except Exception as e:
            logger.error(f"Error retrieving item from inventory: {e}")
            raise

    def get_inventory_summary(self, session: Session):
        """
        Get a summary of the inventory, including the total number of items and categories.
        """
        try:
            # Get the total number of items and categories
            total_items = len(self.items)
            total_categories = len(self.categories)
            return {
                "total_items": total_items,
                "total_categories": total_categories
            }
        except Exception as e:
            logger.error(f"Error getting inventory summary: {e}")
            raise

    def filter_items(self, item_name: str, category_name: str, session: Session):
        """
        Filter items in the inventory by name or category.
        """
        try:
            # Filter items by name or category
            filtered_items = [item for item in self.items if item.name == item_name or item.category.name == category_name]
            return filtered_items
        except Exception as e:
            logger.error(f"Error filtering items in inventory: {e}")
            raise
