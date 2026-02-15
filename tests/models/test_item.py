import pytest
from app.models.item import Item, CATEGORIES
from sqlmodel import select


def test_item_defaults(session):
    """Test creating Item with keyword args."""
    item = Item(name="Toothbrush", category="Other", description="A toothbrush", quantity=1)
    session.add(item)
    session.commit()
    session.refresh(item)
    assert item.id is not None
    assert item.name == "Toothbrush"
    assert item.category == "Other"
    assert item.description == "A toothbrush"
    assert item.quantity == 1


def test_item_optional_fields(session):
    """Test Item with only required fields."""
    item = Item(name="Pen", category="Other")
    session.add(item)
    session.commit()
    session.refresh(item)
    assert item.description is None
    assert item.price == 0.0
    assert item.quantity == 0


def test_item_crud(session):
    """Test full CRUD cycle on Item."""
    # Create
    item = Item(name="Book", category="Books", description="A book", price=9.99, quantity=5)
    session.add(item)
    session.commit()
    session.refresh(item)
    item_id = item.id

    # Read
    retrieved = session.get(Item, item_id)
    assert retrieved is not None
    assert retrieved.name == "Book"
    assert retrieved.price == 9.99

    # Update
    retrieved.quantity = 10
    session.add(retrieved)
    session.commit()
    session.refresh(retrieved)
    assert retrieved.quantity == 10

    # Delete
    session.delete(retrieved)
    session.commit()
    assert session.get(Item, item_id) is None


def test_item_list(session):
    """Test listing multiple items."""
    item1 = Item(name="Item 1", category="Electronics")
    item2 = Item(name="Item 2", category="Clothing")
    session.add(item1)
    session.add(item2)
    session.commit()
    results = session.exec(select(Item)).all()
    assert len(results) == 2


def test_item_categories_constant():
    """Test that CATEGORIES constant exists and has entries."""
    assert isinstance(CATEGORIES, list)
    assert len(CATEGORIES) > 0
    assert "Electronics" in CATEGORIES
    assert "Books" in CATEGORIES