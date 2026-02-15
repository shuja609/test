from app.services.inventory_service import InventoryService
from app.models.inventory import Inventory
import pytest
from uuid import uuid4


@pytest.fixture
def inventory_service(session):
    return InventoryService(session)


async def test_create_item(inventory_service):
    """Test creating a new item."""
    item = Inventory(name="Test Item", category="Electronics")
    created = await inventory_service.create(item)
    assert created.name == "Test Item"
    assert created.category == "Electronics"
    assert created.id is not None


async def test_get_item(inventory_service):
    """Test getting an item by ID."""
    item = Inventory(name="Test Item", category="Electronics")
    created = await inventory_service.create(item)
    retrieved = await inventory_service.get(created.id)
    assert retrieved is not None
    assert retrieved.name == "Test Item"


async def test_get_item_not_found(inventory_service):
    """Test getting an item that doesn't exist."""
    retrieved = await inventory_service.get(uuid4())
    assert retrieved is None


async def test_list_items(inventory_service):
    """Test listing all items."""
    await inventory_service.create(Inventory(name="Item 1", category="Electronics"))
    await inventory_service.create(Inventory(name="Item 2", category="Clothing"))
    items = await inventory_service.list()
    assert len(items) == 2


async def test_update_item(inventory_service):
    """Test updating an existing item."""
    item = Inventory(name="Original", category="Electronics")
    created = await inventory_service.create(item)
    updated = await inventory_service.update(created.id, {"name": "Updated", "category": "Toys"})
    assert updated.name == "Updated"
    assert updated.category == "Toys"


async def test_update_item_not_found(inventory_service):
    """Test updating an item that doesn't exist."""
    updated = await inventory_service.update(uuid4(), {"name": "Updated"})
    assert updated is None


async def test_delete_item(inventory_service):
    """Test deleting an existing item."""
    item = Inventory(name="To Delete", category="Electronics")
    created = await inventory_service.create(item)
    deleted = await inventory_service.delete(created.id)
    assert deleted is True


async def test_delete_item_not_found(inventory_service):
    """Test deleting an item that doesn't exist."""
    deleted = await inventory_service.delete(uuid4())
    assert deleted is False


async def test_search_items_by_name(inventory_service):
    """Test searching items by name."""
    await inventory_service.create(Inventory(name="Alpha", category="Electronics"))
    await inventory_service.create(Inventory(name="Beta", category="Electronics"))
    results = await inventory_service.search(name="Alpha")
    assert len(results) == 1
    assert results[0].name == "Alpha"


async def test_search_items_by_category(inventory_service):
    """Test searching items by category."""
    await inventory_service.create(Inventory(name="Item 1", category="Electronics"))
    await inventory_service.create(Inventory(name="Item 2", category="Toys"))
    results = await inventory_service.search(category="Electronics")
    assert len(results) == 1
    assert results[0].category == "Electronics"


async def test_get_summary(inventory_service):
    """Test getting the summary."""
    await inventory_service.create(Inventory(name="Item 1", category="Electronics"))
    await inventory_service.create(Inventory(name="Item 2", category="Toys"))
    summary = await inventory_service.get_summary()
    assert summary["total_items"] == 2
    assert len(summary["categories"]) == 2


async def test_get_items_by_category(inventory_service):
    """Test getting items by category."""
    await inventory_service.create(Inventory(name="Item 1", category="Electronics"))
    await inventory_service.create(Inventory(name="Item 2", category="Electronics"))
    await inventory_service.create(Inventory(name="Item 3", category="Toys"))
    items = await inventory_service.get_items_by_category("Electronics")
    assert len(items) == 2


async def test_filter_items(inventory_service):
    """Test filtering items."""
    await inventory_service.create(Inventory(name="Alpha", category="Electronics"))
    await inventory_service.create(Inventory(name="Beta", category="Electronics"))
    await inventory_service.create(Inventory(name="Gamma", category="Toys"))
    results = await inventory_service.filter_items(name="Alpha", category="Electronics")
    assert len(results) == 1
    assert results[0].name == "Alpha"