from app.core.database import get_session
from app.exceptions import ItemNotFoundError
from app.models.category import Category
from app.models.inventory import Inventory, Item
from app.models.item import Item
import pytest
from typing import List

# Define a test client and database session
@pytest.fixture
def session():
    return get_session()

def test_create_inventory_defaults(session):
    inventory = Inventory()
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    assert inventory.id is not None
    assert inventory.items == []
    assert inventory.categories == []

def test_inventory_id_max_length(session):
    # SQLModel will automatically limit the length of a string field to the max_length specified
    # In this case, id is limited to 32 characters (uuid4)
    inventory = Inventory(id="a" * 33)
    with pytest.raises(ValueError):
        session.add(inventory)
        session.commit()

def test_inventory_id_nullable(session):
    # Since id is not specified as nullable=False, let's test the default value
    inventory = Inventory()
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    assert inventory.id is not None

def test_item_unique_in_inventory(session):
    # Test that adding an item with the same name will update the existing item's quantity
    item1 = Item(name="Test Item", quantity=1)
    item2 = Item(name="Test Item", quantity=2)
    inventory = Inventory()
    session.add(item1)
    session.add(item2)
    inventory.items.append(item1)
    inventory.items.append(item2)
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    assert len(inventory.items) == 1
    assert inventory.items[0].quantity == 3

def test_item_relationships(session):
    # Test creating a new item and category
    category = Category(name="Test Category")
    item = Item(name="Test Item", category=category)
    session.add(category)
    session.add(item)
    session.commit()
    session.refresh(category)
    session.refresh(item)
    assert category.items == []
    assert item.category == category

def test_inventory_relationships(session):
    # Test creating a new inventory with items and categories
    category1 = Category(name="Test Category 1")
    category2 = Category(name="Test Category 2")
    item1 = Item(name="Test Item 1", category=category1)
    item2 = Item(name="Test Item 2", category=category2)
    inventory = Inventory()
    inventory.items.append(item1)
    inventory.items.append(item2)
    inventory.categories.append(category1)
    inventory.categories.append(category2)
    session.add(inventory)
    session.add(item1)
    session.add(item2)
    session.add(category1)
    session.add(category2)
    session.commit()
    session.refresh(inventory)
    assert len(inventory.items) == 2
    assert len(inventory.categories) == 2

def test_add_item(session):
    # Test adding a new item to the inventory
    category = Category(name="Test Category")
    item = Item(name="Test Item", category=category)
    inventory = Inventory()
    session.add(item)
    session.add(category)
    session.commit()
    session.refresh(item)
    session.refresh(inventory)
    inventory.add_item(item, session)
    session.refresh(inventory)
    assert len(inventory.items) == 1
    assert inventory.items[0] == item

def test_update_item(session):
    # Test updating an existing item in the inventory
    category = Category(name="Test Category")
    item = Item(name="Test Item", category=category, quantity=1)
    inventory = Inventory()
    session.add(item)
    session.add(category)
    session.commit()
    session.refresh(item)
    inventory.add_item(item, session)
    session.refresh(inventory)
    inventory.update_item(item.id, 2, "New description", session)
    session.refresh(inventory)
    session.refresh(item)
    assert len(inventory.items) == 1
    assert inventory.items[0].quantity == 2
    assert inventory.items[0].description == "New description"

def test_retrieve_item(session):
    # Test retrieving an existing item from the inventory
    category = Category(name="Test Category")
    item = Item(name="Test Item", category=category)
    inventory = Inventory()
    session.add(item)
    session.add(category)
    session.commit()
    session.refresh(item)
    inventory.add_item(item, session)
    session.refresh(inventory)
    retrieved_item = inventory.retrieve_item(item.name, session)
    assert retrieved_item.id == item.id
    assert retrieved_item.name == item.name

def test_get_inventory_summary(session):
    # Test getting the inventory summary
    category1 = Category(name="Test Category 1")
    category2 = Category(name="Test Category 2")
    item1 = Item(name="Test Item 1", category=category1)
    item2 = Item(name="Test Item 2", category=category2)
    inventory = Inventory()
    session.add(item1)
    session.add(item2)
    session.add(category1)
    session.add(category2)
    session.commit()
    session.refresh(item1)
    session.refresh(item2)
    session.refresh(category1)
    session.refresh(category2)
    inventory.add_item(item1, session)
    inventory.add_item(item2, session)
    inventory.categories.append(category1)
    inventory.categories.append(category2)
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    summary = inventory.get_inventory_summary(session)
    assert summary["total_items"] == 2
    assert summary["total_categories"] == 2

def test_filter_items(session):
    # Test filtering items in the inventory
    category1 = Category(name="Test Category 1")
    category2 = Category(name="Test Category 2")
    item1 = Item(name="Test Item 1", category=category1)
    item2 = Item(name="Test Item 2", category=category2)
    item3 = Item(name="Test Item 3", category=category1)
    inventory = Inventory()
    session.add(item1)
    session.add(item2)
    session.add(item3)
    session.add(category1)
    session.add(category2)
    session.commit()
    session.refresh(item1)
    session.refresh(item2)
    session.refresh(item3)
    session.refresh(category1)
    session.refresh(category2)
    inventory.add_item(item1, session)
    inventory.add_item(item2, session)
    inventory.add_item(item3, session)
    session.commit()
    session.refresh(inventory)
    filtered_items = inventory.filter_items("Test Item 1", None, session)
    assert len(filtered_items) == 1
    assert filtered_items[0].name == "Test Item 1"
    filtered_items = inventory.filter_items(None, "Test Category 1", session)
    assert len(filtered_items) == 2
    assert filtered_items[0].name == "Test Item 1"
    assert filtered_items[1].name == "Test Item 3"

def test_delete_item(session):
    # Test deleting an existing item from the inventory
    category = Category(name="Test Category")
    item = Item(name="Test Item", category=category)
    inventory = Inventory()
    session.add(item)
    session.add(category)
    session.commit()
    session.refresh(item)
    inventory.add_item(item, session)
    session.commit()
    session.refresh(inventory)
    assert len(inventory.items) == 1
    session.delete(item)
    session.commit()
    session.refresh(inventory)
    assert len(inventory.items) == 0