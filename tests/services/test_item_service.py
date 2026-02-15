from app.services.item_service import ItemService
from app.exceptions import InvalidCategoryError, ItemNotFoundError
from app.models.item import Item, CATEGORIES
import pytest


@pytest.fixture
def item_service(session):
    return ItemService(session)


async def test_create_item_valid(item_service):
    """Test creating a valid item."""
    item = Item(name="Test Item", category=CATEGORIES[0], description="Test desc")
    created = await item_service.create(item)
    assert created.name == "Test Item"
    assert created.category == CATEGORIES[0]
    assert created.id is not None


async def test_create_item_invalid_category(item_service):
    """Test creating item with invalid category."""
    item = Item(name="Test Item", category="Invalid Category", description="Test")
    with pytest.raises(InvalidCategoryError, match="Invalid category"):
        await item_service.create(item)


async def test_create_item_empty_name(item_service):
    """Test creating item with empty name (allowed by model)."""
    item = Item(name="", category=CATEGORIES[0], description="Test")
    result = await item_service.create(item)
    assert result.name == ""


async def test_get_item(item_service):
    """Test getting an item by ID."""
    item = Item(name="Test Item", category=CATEGORIES[0], description="Test")
    created = await item_service.create(item)
    retrieved = await item_service.get(created.id)
    assert retrieved is not None
    assert retrieved.name == "Test Item"


async def test_get_item_not_found(item_service):
    """Test getting non-existent item returns None."""
    from uuid import uuid4
    result = await item_service.get(uuid4())
    assert result is None


async def test_list_items(item_service):
    """Test listing items."""
    await item_service.create(Item(name="Item 1", category=CATEGORIES[0], description="D1"))
    await item_service.create(Item(name="Item 2", category=CATEGORIES[0], description="D2"))
    items = await item_service.list()
    assert len(items) >= 2


async def test_update_item_valid(item_service):
    """Test updating an item."""
    item = Item(name="Original", category=CATEGORIES[0], description="Test")
    created = await item_service.create(item)
    updated = await item_service.update(created.id, {"name": "Updated"})
    assert updated.name == "Updated"


async def test_update_item_invalid_category(item_service):
    """Test updating item with invalid category."""
    item = Item(name="Test", category=CATEGORIES[0], description="Test")
    created = await item_service.create(item)
    with pytest.raises(InvalidCategoryError, match="Invalid category"):
        await item_service.update(created.id, {"category": "Invalid"})


async def test_delete_item(item_service):
    """Test deleting an item."""
    item = Item(name="To Delete", category=CATEGORIES[0], description="Test")
    created = await item_service.create(item)
    deleted = await item_service.delete(created.id)
    assert deleted is True


async def test_filter_items_by_name(item_service):
    """Test filtering items by name."""
    await item_service.create(Item(name="Test Item 1", category=CATEGORIES[0], description="D1"))
    await item_service.create(Item(name="Test Item 2", category=CATEGORIES[0], description="D2"))
    results = await item_service.filter(name="Test Item 1")
    assert len(results) >= 1


async def test_filter_items_by_category(item_service):
    """Test filtering items by category."""
    await item_service.create(Item(name="Item 1", category=CATEGORIES[0], description="D1"))
    await item_service.create(Item(name="Item 2", category=CATEGORIES[1], description="D2"))
    results = await item_service.filter(category=CATEGORIES[0])
    assert len(results) >= 1


async def test_filter_items_invalid_category(item_service):
    """Test filtering with invalid category."""
    with pytest.raises(InvalidCategoryError, match="Invalid category"):
        await item_service.filter(category="Invalid Category")


async def test_get_categories(item_service):
    """Test getting categories list."""
    categories = await item_service.get_categories()
    assert len(categories) == len(CATEGORIES)


async def test_get_item_summary(item_service):
    """Test getting item summary."""
    await item_service.create(Item(name="Item 1", category=CATEGORIES[0], description="D1"))
    await item_service.create(Item(name="Item 2", category=CATEGORIES[1], description="D2"))
    summary = await item_service.get_item_summary()
    assert summary["total_items"] >= 2
    assert summary["categories"][CATEGORIES[0]] >= 1
    assert summary["categories"][CATEGORIES[1]] >= 1