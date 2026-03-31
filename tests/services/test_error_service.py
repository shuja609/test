from app.core.database import get_session
from app.exceptions import HTTPException
from app.services.error_service import ErrorService
from app.models.error import Error

import pytest
from uuid import UUID
import logging

# Define logging configuration
logging.basicConfig(level=logging.INFO)

@pytest.fixture
def error_service(session):
    return ErrorService(session)

async def test_create_item(error_service: ErrorService):
    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    created_item = await error_service.create(item)
    assert item.name == created_item.name
    assert item.category == created_item.category
    assert item.description == created_item.description
    assert item.quantity == created_item.quantity

async def test_create_item_empty_name(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.create(Error(name="", category="Test Category", description="Test Description", quantity=10))
    assert exc.value.status_code == 400

async def test_create_item_invalid_quantity(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.create(Error(name="Test Item", category="Test Category", description="Test Description", quantity=-1))
    assert exc.value.status_code == 400

async def test_get_item(error_service: ErrorService):
    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    created_item = await error_service.create(item)
    fetched_item = await error_service.get(created_item.id)
    assert fetched_item.name == created_item.name
    assert fetched_item.category == created_item.category
    assert fetched_item.description == created_item.description
    assert fetched_item.quantity == created_item.quantity

async def test_get_item_non_existent(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.get(UUID("12345678-1234-1234-1234-123456789012"))
    assert exc.value.status_code == 404

async def test_list_items(error_service: ErrorService):
    item1 = Error(name="Test Item 1", category="Test Category", description="Test Description", quantity=10)
    item2 = Error(name="Test Item 2", category="Test Category", description="Test Description", quantity=20)
    await error_service.create(item1)
    await error_service.create(item2)
    items = await error_service.list()
    assert len(items) == 2

async def test_list_items_empty(error_service: ErrorService):
    items = await error_service.list()
    assert len(items) == 0

async def test_update_item(error_service: ErrorService):
    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    created_item = await error_service.create(item)
    updated_item = await error_service.update(created_item.id, {"name": "Updated Test Item", "quantity": 20})
    assert updated_item.name == "Updated Test Item"
    assert updated_item.quantity == 20

async def test_update_item_non_existent(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.update(UUID("12345678-1234-1234-1234-123456789012"), {"name": "Updated Test Item"})
    assert exc.value.status_code == 404

async def test_delete_item(error_service: ErrorService):
    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    created_item = await error_service.create(item)
    success = await error_service.delete(created_item.id)
    assert success

async def test_delete_item_non_existent(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.delete(UUID("12345678-1234-1234-1234-123456789012"))
    assert exc.value.status_code == 404

async def test_validate_item(error_service: ErrorService):
    item = Error(name="Test Item", category="Test Category", description="Test Description", quantity=10)
    validated_item = await error_service.validate_item(item)
    assert validated_item.name == item.name
    assert validated_item.category == item.category
    assert validated_item.description == item.description
    assert validated_item.quantity == item.quantity

async def test_validate_item_empty_name(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.validate_item(Error(name="", category="Test Category", description="Test Description", quantity=10))
    assert exc.value.status_code == 400

async def test_validate_unique_item(error_service: ErrorService):
    await error_service.validate_unique_item("Test Item", "Test Category")
    with pytest.raises(HTTPException) as exc:
        await error_service.validate_unique_item("Test Item", "Test Category")
    assert exc.value.status_code == 400

async def test_handle_system_error(error_service: ErrorService):
    with pytest.raises(HTTPException) as exc:
        await error_service.handle_system_error()
    assert exc.value.status_code == 500