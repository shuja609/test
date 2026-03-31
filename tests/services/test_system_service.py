from app.core.database import get_session
from app.exceptions import (
    ResourceNotFound,
    InvalidRequest,
    AlreadyExists
)
from app.services.system_service import SystemService
from app.models.system import System
import pytest
import uuid

# Create a test system item
@pytest.fixture
def test_system_item(session):
    item = System(id=uuid.uuid4(), name="Test System", description="Test System Description")
    session.add(item)
    session.commit()
    session.refresh(item)
    yield item
    session.delete(item)
    session.commit()

# Test create system item
async def test_create_system_item(session):
    service = SystemService(session)
    item = System(id=uuid.uuid4(), name="New System", description="New System Description")
    created_item = await service.create(item)
    assert created_item.name == "New System"
    assert created_item.description == "New System Description"
    # Clean up
    session.delete(item)
    session.commit()

# Test get system item
async def test_get_system_item(session, test_system_item):
    service = SystemService(session)
    retrieved_item = await service.get(test_system_item.id)
    assert retrieved_item.name == test_system_item.name
    assert retrieved_item.description == test_system_item.description

# Test get non-existent system item
async def test_get_non_existent_system_item(session):
    service = SystemService(session)
    retrieved_item = await service.get(uuid.uuid4())
    assert retrieved_item is None

# Test list system items
async def test_list_system_items(session, test_system_item):
    service = SystemService(session)
    # Add another test system item
    item = System(id=uuid.uuid4(), name="Another Test System", description="Another Test System Description")
    session.add(item)
    session.commit()
    session.refresh(item)
    # Get list of system items
    listed_items = await service.list()
    assert len(listed_items) >= 2
    # Clean up
    session.delete(item)
    session.commit()

# Test update system item
async def test_update_system_item(session, test_system_item):
    service = SystemService(session)
    updated_item = await service.update(test_system_item.id, {"name": "Updated Test System", "description": "Updated Test System Description"})
    assert updated_item.name == "Updated Test System"
    assert updated_item.description == "Updated Test System Description"

# Test update non-existent system item
async def test_update_non_existent_system_item(session):
    service = SystemService(session)
    updated_item = await service.update(uuid.uuid4(), {"name": "Updated Test System", "description": "Updated Test System Description"})
    assert updated_item is None

# Test delete system item
async def test_delete_system_item(session, test_system_item):
    service = SystemService(session)
    deleted = await service.delete(test_system_item.id)
    assert deleted
    # Try to get deleted item
    retrieved_item = await service.get(test_system_item.id)
    assert retrieved_item is None

# Test delete non-existent system item
async def test_delete_non_existent_system_item(session):
    service = SystemService(session)
    deleted = await service.delete(uuid.uuid4())
    assert not deleted

# Test create duplicate system item
async def test_create_duplicate_system_item(session, test_system_item):
    service = SystemService(session)
    duplicate_item = System(id=uuid.uuid4(), name=test_system_item.name, description=test_system_item.description)
    with pytest.raises(AlreadyExists):
        await service.create(duplicate_item)

# Test invalid system item
async def test_create_invalid_system_item(session):
    service = SystemService(session)
    invalid_item = System(id=None, name=None, description=None)
    with pytest.raises(InvalidRequest):
        await service.create(invalid_item)

# Test update system item with invalid data
async def test_update_system_item_with_invalid_data(session, test_system_item):
    service = SystemService(session)
    with pytest.raises(InvalidRequest):
        await service.update(test_system_item.id, {"name": None, "description": None})