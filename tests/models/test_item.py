from app.core.database import get_session
from app.models.item import Item, Inventory, CATEGORIES
import pytest
from app.exceptions import NotFound, Conflict

def test_item_defaults():
    """Test Item model defaults"""
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    assert item.id is not None
    assert item.name == "Toothbrush"
    assert item.description == "A toothbrush for cleaning teeth"
    assert item.category in CATEGORIES
    assert item.quantity == 1

def test_item_validation(session):
    """Test Item model validation"""
    # Test name max length (not explicitly defined in the code, assuming 100 characters)
    with pytest.raises(ValueError):
        Item("a" * 101, "A toothbrush for cleaning teeth", "toiletries", 1)

    # Test description max length (not explicitly defined in the code, assuming 500 characters)
    with pytest.raises(ValueError):
        Item("Toothbrush", "a" * 501, "toiletries", 1)

    # Test quantity non-negative
    with pytest.raises(ValueError):
        Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", -1)

def test_item_unique_id(session):
    """Test Item model unique id"""
    # Test creating two items with the same id (not possible with uuid)
    item1 = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    item2 = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    assert item1.id != item2.id

def test_inventory_relationships(session):
    """Test Inventory model relationships"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    assert item in inventory.items

def test_create_item(session):
    """Test creating a new Item model"""
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    session.add(item)  # Note: session.add is not applicable for this Item model
    # Instead, use inventory.add_item_to_inventory(item)
    inventory = Inventory()
    inventory.add_item_to_inventory(item)

def test_read_item(session):
    """Test reading an Item model"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    assert item in inventory.items

def test_update_item(session):
    """Test updating an Item model"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    item.update_item(new_quantity=2)
    assert item.quantity == 2

def test_delete_item(session):
    """Test deleting an Item model"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    inventory.delete_item_from_inventory(item.id)
    assert item not in inventory.items

def test_inventory_get_item_details(session):
    """Test getting Item details from Inventory"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    item_details = inventory.get_item_details_from_inventory(item.id)
    assert item_details["id"] == item.id
    assert item_details["name"] == item.name
    assert item_details["description"] == item.description
    assert item_details["category"] == item.category
    assert item_details["quantity"] == item.quantity

def test_inventory_update_item(session):
    """Test updating Item in Inventory"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    inventory.update_item_in_inventory(item.id, new_quantity=2)
    assert item.quantity == 2

def test_inventory_delete_item(session):
    """Test deleting Item from Inventory"""
    inventory = Inventory()
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    inventory.add_item_to_inventory(item)
    inventory.delete_item_from_inventory(item.id)
    assert item not in inventory.items

def test_item_str(session):
    """Test Item model string representation"""
    item = Item("Toothbrush", "A toothbrush for cleaning teeth", "toiletries", 1)
    assert str(item) == f"Item(id={item.id}, name=Toothbrush, description=A toothbrush for cleaning teeth, category=toiletries, quantity=1)"