import uuid
from typing import Optional
import logging

# Define categories
CATEGORIES = ["toiletries", "electronics", "clothing"]

class Item:
    """
    Item model.
    """
    def __init__(self, name: str, description: str, category: str, quantity: int):
        """
        Initialize the Item model.
        
        Args:
        name (str): The name of the item.
        description (str): A brief description of the item.
        category (str): The category of the item (e.g., toiletries, electronics, clothing).
        quantity (int): The quantity of the item.
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.category = category
        self.quantity = quantity

    def __str__(self):
        return f"Item(id={self.id}, name={self.name}, description={self.description}, category={self.category}, quantity={self.quantity})"

    def add_item(self) -> None:
        """
        Add a new item to the inventory.
        
        Returns:
        None
        """
        try:
            logging.info(f"Adding item {self.name} to inventory")
        except Exception as e:
            logging.error(f"Error adding item {self.name} to inventory: {str(e)}")

    def update_item(self, new_name: Optional[str] = None, new_description: Optional[str] = None, new_category: Optional[str] = None, new_quantity: Optional[int] = None) -> None:
        """
        Update an existing item in the inventory.
        
        Args:
        new_name (str): The new name of the item (optional).
        new_description (str): A new brief description of the item (optional).
        new_category (str): The new category of the item (e.g., toiletries, electronics, clothing) (optional).
        new_quantity (int): The new quantity of the item (optional).
        
        Returns:
        None
        """
        try:
            if new_name:
                self.name = new_name
            if new_description:
                self.description = new_description
            if new_category in CATEGORIES:
                self.category = new_category
            if new_quantity:
                self.quantity = new_quantity
            logging.info(f"Updated item {self.name} in inventory")
        except Exception as e:
            logging.error(f"Error updating item {self.name} in inventory: {str(e)}")

    def delete_item(self) -> None:
        """
        Delete an item from the inventory.
        
        Returns:
        None
        """
        try:
            logging.info(f"Deleting item {self.name} from inventory")
        except Exception as e:
            logging.error(f"Error deleting item {self.name} from inventory: {str(e)}")

    def get_item_details(self) -> dict:
        """
        Get the details of an item.
        
        Returns:
        dict: A dictionary containing the item's details.
        """
        try:
            item_details = {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "category": self.category,
                "quantity": self.quantity
            }
            logging.info(f"Retrieved item {self.name} details")
            return item_details
        except Exception as e:
            logging.error(f"Error retrieving item {self.name} details: {str(e)}")
            return {}

class Inventory:
    def __init__(self):
        self.items = []

    def add_item_to_inventory(self, item: Item) -> None:
        """
        Add a new item to the inventory.
        
        Args:
        item (Item): The item to add to the inventory.
        
        Returns:
        None
        """
        try:
            self.items.append(item)
            logging.info(f"Added item {item.name} to inventory")
        except Exception as e:
            logging.error(f"Error adding item {item.name} to inventory: {str(e)}")

    def update_item_in_inventory(self, item_id: str, new_name: Optional[str] = None, new_description: Optional[str] = None, new_category: Optional[str] = None, new_quantity: Optional[int] = None) -> None:
        """
        Update an existing item in the inventory.
        
        Args:
        item_id (str): The ID of the item to update.
        new_name (str): The new name of the item (optional).
        new_description (str): A new brief description of the item (optional).
        new_category (str): The new category of the item (e.g., toiletries, electronics, clothing) (optional).
        new_quantity (int): The new quantity of the item (optional).
        
        Returns:
        None
        """
        try:
            for item in self.items:
                if item.id == item_id:
                    item.update_item(new_name, new_description, new_category, new_quantity)
                    logging.info(f"Updated item {item.name} in inventory")
                    return
            logging.error(f"Item with ID {item_id} not found in inventory")
        except Exception as e:
            logging.error(f"Error updating item {item_id} in inventory: {str(e)}")

    def delete_item_from_inventory(self, item_id: str) -> None:
        """
        Delete an item from the inventory.
        
        Args:
        item_id (str): The ID of the item to delete.
        
        Returns:
        None
        """
        try:
            for item in self.items:
                if item.id == item_id:
                    self.items.remove(item)
                    logging.info(f"Deleted item {item.name} from inventory")
                    return
            logging.error(f"Item with ID {item_id} not found in inventory")
        except Exception as e:
            logging.error(f"Error deleting item {item_id} from inventory: {str(e)}")

    def get_item_details_from_inventory(self, item_id: str) -> dict:
        """
        Get the details of an item from the inventory.
        
        Args:
        item_id (str): The ID of the item to retrieve details for.
        
        Returns:
        dict: A dictionary containing the item's details.
        """
        try:
            for item in self.items:
                if item.id == item_id:
                    return item.get_item_details()
            logging.error(f"Item with ID {item_id} not found in inventory")
            return {}
        except Exception as e:
            logging.error(f"Error retrieving item {item_id} details: {str(e)}")
            return {}

# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create a new inventory
    inventory = Inventory()
    
    # Create a new item
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    
    # Add the item to the inventory
    inventory.add_item_to_inventory(item)
    
    # Update the item in the inventory
    inventory.update_item_in_inventory(item.id, new_quantity=2)
    
    # Get the item's details from the inventory
    item_details = inventory.get_item_details_from_inventory(item.id)
    print(item_details)
    
    # Delete the item from the inventory
    inventory.delete_item_from_inventory(item.id)
