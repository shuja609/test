from app.models.system import System
from app.services.system_service import SystemService
import pytest
from datetime import datetime


@pytest.fixture
def system_service(session):
    return SystemService(session)


def _make_system(**kwargs):
    """Helper to create System with required fields."""
    defaults = {"version": "1.0.0", "lastUpdated": datetime.utcnow()}
    defaults.update(kwargs)
    return System(**defaults)


async def test_create_system(system_service):
    """Test creating a system."""
    system = _make_system(version="1.0.0")
    created = await system_service.create(system)
    assert created.version == "1.0.0"
    assert created.id is not None


async def test_get_system(system_service):
    """Test getting a system by ID."""
    system = _make_system()
    created = await system_service.create(system)
    retrieved = await system_service.get(created.id)
    assert retrieved is not None
    assert retrieved.version == system.version


async def test_list_systems(system_service):
    """Test listing systems."""
    await system_service.create(_make_system(version="1.0"))
    await system_service.create(_make_system(version="2.0"))
    systems = await system_service.list()
    assert len(systems) == 2


async def test_update_system(system_service):
    """Test updating a system."""
    system = _make_system()
    created = await system_service.create(system)
    updated = await system_service.update(created.id, {"version": "2.0.0"})
    assert updated.version == "2.0.0"


async def test_delete_system(system_service):
    """Test deleting a system."""
    system = _make_system()
    created = await system_service.create(system)
    deleted = await system_service.delete(created.id)
    assert deleted is True
    retrieved = await system_service.get(created.id)
    assert retrieved is None


async def test_get_nonexistent_system(system_service):
    """Test getting a non-existent system returns None."""
    retrieved = await system_service.get(99999)
    assert retrieved is None


async def test_update_nonexistent_system(system_service):
    """Test updating a non-existent system returns None."""
    updated = await system_service.update(99999, {"version": "2.0"})
    assert updated is None


async def test_delete_nonexistent_system(system_service):
    """Test deleting a non-existent system returns False."""
    deleted = await system_service.delete(99999)
    assert deleted is False


async def test_create_system_with_all_fields(system_service):
    """Test creating system with all fields explicitly set."""
    now = datetime.utcnow()
    system = System(version="3.0.0", lastUpdated=now)
    created = await system_service.create(system)
    assert created.version == "3.0.0"
    assert created.lastUpdated == now