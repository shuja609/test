import pytest
from app.core.database import get_session
from app.exceptions import InvalidCategoryError, ItemNotFoundError
from app.models.item import Item, CATEGORIES
from app.services.item_service import ItemService

@pytest.fixture
async def session():
    async with get_session() as session:
        yield session

@pytest.fixture
async def item_service(session):
    return ItemService(session)

async def test_create_item_valid_category(item_service):
    item = Item(name="Test Item", category=CATEGORIES[0])
    created_item = await item_service.create(item)
    assert created_item.name == item.name
    assert created_item.category == item.category

async def test_create_item_invalid_category(item_service):
    item = Item(name="Test Item", category="Invalid Category")
    with pytest.raises(InvalidCategoryError, match="Invalid category"):
        await item_service.create(item)

async def test_get_item(item_service):
    item = Item(name="Test Item", category=CATEGORIES[0])
    await item_service.session.add(item)
    await item_service.session.commit()
    await item_service.session.refresh(item)
    db_item = await item_service.get(item.id)
    assert db_item.name == item.name
    assert db_item.category == item.category

async def test_get_item_not_found(item_service):
    db_item = await item_service.get(UUID("00000000-0000-0000-0000-000000000000"))
    assert db_item is None

async def test_list_items(item_service):
    for i in range(10):
        item = Item(name=f"Test Item {i}", category=CATEGORIES[0])
        await item_service.session.add(item)
    await item_service.session.commit()
    items = await item_service.list()
    assert len(items) == 10

async def test_update_item(item_service):
    item = Item(name="Test Item", category=CATEGORIES[0])
    await item_service.session.add(item)
    await item_service.session.commit()
    await item_service.session.refresh(item)
    updated_item = await item_service.update(item.id, {"name": "Updated Item"})
    assert updated_item.name == "Updated Item"

async def test_update_item_invalid_category(item_service):
    item = Item(name="Test Item", category=CATEGORIES[0])
    await item_service.session.add(item)
    await item_service.session.commit()
    await item_service.session.refresh(item)
    with pytest.raises(InvalidCategoryError, match="Invalid category"):
        await item_service.update(item.id, {"category": "Invalid Category"})

async def test_delete_item(item_service):
    item = Item(name="Test Item", category=CATEGORIES[0])
    await item_service.session.add(item)
    await item_service.session.commit()
    await item_service.session.refresh(item)
    deleted = await item_service.delete(item.id)
    assert deleted

async def test_delete_item_not_found(item_service):
    with pytest.raises(ItemNotFoundError, match="Item not found"):
        await item_service.delete(UUID("00000000-0000-0000-0000-000000000000"))

async def test_filter_items_by_name(item_service):
    item1 = Item(name="Test Item 1", category=CATEGORIES[0])
    item2 = Item(name="Test Item 2", category=CATEGORIES[0])
    await item_service.session.add_all([item1, item2])
    await item_service.session.commit()
    items = await item_service.filter(name="Item 1")
    assert len(items) == 1

async def test_filter_items_by_category(item_service):
    item1 = Item(name="Test Item 1", category=CATEGORIES[0])
    item2 = Item(name="Test Item 2", category=CATEGORIES[1])
    await item_service.session.add_all([item1, item2])
    await item_service.session.commit()
    items = await item_service.filter(category=CATEGORIES[0])
    assert len(items) == 1

async def test_get_categories(item_service):
    categories = await item_service.get_categories()
    assert categories == CATEGORIES

async def test_get_item_summary(item_service):
    for i in range(10):
        item = Item(name=f"Test Item {i}", category=CATEGORIES[0])
        await item_service.session.add(item)
    for i in range(5):
        item = Item(name=f"Test Item {i}", category=CATEGORIES[1])
        await item_service.session.add(item)
    await item_service.session.commit()
    summary = await item_service.get_item_summary()
    assert summary["total_items"] == 15
    assert summary["categories"][CATEGORIES[0]] == 10
    assert summary["categories"][CATEGORIES[1]] == 5