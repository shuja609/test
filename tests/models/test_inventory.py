from app.models.inventory import Inventory
import pytest
from sqlmodel import Session, select


def test_inventory_defaults(session: Session):
    """Test that required fields must be provided."""
    inventory = Inventory(name="Test Item", category="Electronics")
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    assert inventory.id is not None
    assert inventory.name == "Test Item"
    assert inventory.category == "Electronics"
    assert inventory.description is None
    assert inventory.quantity == 0


def test_inventory_create_item(session: Session):
    """Test creating a new inventory item with all fields."""
    item = Inventory(name="Widget", category="Electronics", description="A widget", quantity=10)
    session.add(item)
    session.commit()
    session.refresh(item)
    assert item.id is not None
    assert item.name == "Widget"
    assert item.quantity == 10


def test_inventory_update_item(session: Session):
    """Test updating an existing inventory item."""
    item = Inventory(name="Widget", category="Electronics", quantity=10)
    session.add(item)
    session.commit()
    session.refresh(item)
    item.quantity = 20
    item.description = "Updated description"
    session.add(item)
    session.commit()
    session.refresh(item)
    assert item.quantity == 20
    assert item.description == "Updated description"


def test_inventory_retrieve_item(session: Session):
    """Test retrieving an inventory item."""
    item = Inventory(name="Widget", category="Electronics", quantity=5)
    session.add(item)
    session.commit()
    retrieved = session.get(Inventory, item.id)
    assert retrieved is not None
    assert retrieved.name == "Widget"
    assert retrieved.quantity == 5


def test_inventory_delete_item(session: Session):
    """Test deleting an inventory item."""
    item = Inventory(name="Widget", category="Electronics")
    session.add(item)
    session.commit()
    item_id = item.id
    session.delete(item)
    session.commit()
    assert session.get(Inventory, item_id) is None


def test_inventory_list_items(session: Session):
    """Test listing multiple inventory items."""
    item1 = Inventory(name="Item 1", category="Electronics")
    item2 = Inventory(name="Item 2", category="Clothing")
    session.add(item1)
    session.add(item2)
    session.commit()
    results = session.exec(select(Inventory)).all()
    assert len(results) == 2


def test_inventory_filter_by_category(session: Session):
    """Test filtering inventory by category."""
    item1 = Inventory(name="Item 1", category="Electronics")
    item2 = Inventory(name="Item 2", category="Clothing")
    session.add(item1)
    session.add(item2)
    session.commit()
    results = session.exec(select(Inventory).where(Inventory.category == "Electronics")).all()
    assert len(results) == 1
    assert results[0].name == "Item 1"