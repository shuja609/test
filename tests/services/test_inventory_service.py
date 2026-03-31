import pytest
from app.core.database import get_session
from app.exceptions import ItemNotFoundError, InvalidItemError
from app.services.inventory_service import InventoryService
from app.models.inventory import Inventory

async def test_create_item(session):
    service = InventoryService(session)
    item = Inventory(name="Test Item", category="Test Category")
    created_item = await service.create(item)
    assert created_item.name == item.name
    assert created_item.category == item.category

async def test_create_item_empty_name(session):
    service = InventoryService(session)
    item = Inventory(name="", category="Test Category")
    with pytest.raises(InvalidItemError):
        await service.create(item)

async def test_get_item(session):
    service = InventoryService(session)
    item = Inventory(name="Test Item", category="Test Category")
    created_item = await service.create(item)
    retrieved_item = await service.get(created_item.id)
    assert retrieved_item.name == created_item.name
    assert retrieved_item.category == created_item.category

async def test_get_item_not_found(session):
    service = InventoryService(session)
    with pytest.raises(ItemNotFoundError):
        await service.get(UUID("00000000-0000-0000-0000-000000000000"))

async def test_list_items(session):
    service = InventoryService(session)
    item1 = Inventory(name="Test Item 1", category="Test Category 1")
    item2 = Inventory(name="Test Item 2", category="Test Category 2")
    await service.create(item1)
    await service.create(item2)
    items = await service.list()
    assert len(items) == 2

async def test_list_items_empty(session):
    service = InventoryService(session)
    items = await service.list()
    assert len(items) == 0

async def test_update_item(session):
    service = InventoryService(session)
    item = Inventory(name="Test Item", category="Test Category")
    created_item = await service.create(item)
    updated_item = await service.update(created_item.id, {"name": "Updated Item"})
    assert updated_item.name == "Updated Item"
    assert updated_item.category == created_item.category

async def test_update_item_not_found(session):
    service = InventoryService(session)
    with pytest.raises(ItemNotFoundError):
        await service.update(UUID("00000000-0000-0000-0000-000000000000"), {"name": "Updated Item"})

async def test_delete_item(session):
    service = InventoryService(session)
    item = Inventory(name="Test Item", category="Test Category")
    created_item = await service.create(item)
    deleted = await service.delete(created_item.id)
    assert deleted
    with pytest.raises(ItemNotFoundError):
        await service.get(created_item.id)

async def test_delete_item_not_found(session):
    service = InventoryService(session)
    with pytest.raises(ItemNotFoundError):
        await service.delete(UUID("00000000-0000-0000-0000-000000000000"))

async def test_search_item(session):
    service = InventoryService(session)
    item = Inventory(name="Test Item", category="Test Category")
    await service.create(item)
    items = await service.search(name="Test Item")
    assert len(items) == 1

async def test_search_item_not_found(session):
    service = InventoryService(session)
    items = await service.search(name="Non-Existent Item")
    assert len(items) == 0

async def test_get_summary(session):
    service = InventoryService(session)
    item1 = Inventory(name="Test Item 1", category="Test Category 1")
    item2 = Inventory(name="Test Item 2", category="Test Category 2")
    await service.create(item1)
    await service.create(item2)
    summary = await service.get_summary()
    assert summary["total_items"] == 2
    assert len(summary["categories"]) == 2

async def test_get_items_by_category(session):
    service = InventoryService(session)
    item1 = Inventory(name="Test Item 1", category="Test Category 1")
    item2 = Inventory(name="Test Item 2", category="Test Category 1")
    await service.create(item1)
    await service.create(item2)
    items = await service.get_items_by_category("Test Category 1")
    assert len(items) == 2

async def test_filter_items(session):
    service = InventoryService(session)
    item1 = Inventory(name="Test Item 1", category="Test Category 1")
    item2 = Inventory(name="Test Item 2", category="Test Category 1")
    await service.create(item1)
    await service.create(item2)
    items = await service.filter_items(name="Test Item 1")
    assert len(items) == 1

async def test_filter_items_no_results(session):
    service = InventoryService(session)
    items = await service.filter_items(name="Non-Existent Item")
    assert len(items) == 0