from app.services.error_service import ErrorService
from app.models.error import Error
from fastapi import HTTPException
import pytest


@pytest.fixture
def error_service(session):
    return ErrorService(session)


async def test_create_error(error_service):
    """Test creating an error item."""
    item = Error(message="Test error", code=400)
    created = await error_service.create(item)
    assert created.id is not None
    assert created.message == "Test error"
    assert created.code == 400


async def test_get_error(error_service):
    """Test getting an error by ID."""
    item = Error(message="Test error", code=500)
    created = await error_service.create(item)
    retrieved = await error_service.get(created.id)
    assert retrieved is not None
    assert retrieved.message == "Test error"


async def test_list_errors(error_service):
    """Test listing errors."""
    await error_service.create(Error(message="Error 1", code=400))
    await error_service.create(Error(message="Error 2", code=500))
    errors = await error_service.list()
    assert len(errors) == 2


async def test_update_error(error_service):
    """Test updating an error."""
    item = Error(message="Original", code=400)
    created = await error_service.create(item)
    updated = await error_service.update(created.id, {"message": "Updated"})
    assert updated.message == "Updated"


async def test_delete_error(error_service):
    """Test deleting an error."""
    item = Error(message="To delete", code=500)
    created = await error_service.create(item)
    deleted = await error_service.delete(created.id)
    assert deleted is True


async def test_delete_nonexistent_error(error_service):
    """Test deleting a non-existent error returns False."""
    deleted = await error_service.delete(999)
    assert deleted is False


async def test_handle_system_error(error_service):
    """Test handle_system_error raises HTTPException."""
    with pytest.raises(HTTPException) as exc:
        await error_service.handle_system_error()
    assert exc.value.status_code == 500