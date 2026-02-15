import pytest
from app.models.system import System, SystemBase, SystemCreate, SystemUpdate, create_system, update_system, read_system
from datetime import datetime
from pydantic import ValidationError


def test_system_model_field_validation():
    """Test SystemBase schema validation."""
    system = SystemBase(version="v1", lastUpdated=datetime.now())
    assert isinstance(system.version, str)

    # version is required
    with pytest.raises((TypeError, ValidationError)):
        SystemBase(lastUpdated=datetime.now())


def test_system_defaults(session):
    """Test that System gets auto-generated int id."""
    system = SystemCreate(version="v1", lastUpdated=datetime.now())
    system_obj = create_system(session, system)
    assert isinstance(system_obj.id, int)


def test_system_crud(session):
    """Test full CRUD cycle using model-level functions."""
    now = datetime.now()
    # Create
    system = SystemCreate(version="v1", lastUpdated=now)
    created = create_system(session, system)
    assert isinstance(created, System)
    assert created.version == "v1"

    # Read
    read_obj = read_system(session, created.id)
    assert isinstance(read_obj, System)
    assert read_obj.id == created.id

    # Update
    updated_data = SystemUpdate(version="v2", lastUpdated=datetime.now())
    updated = update_system(session, created.id, updated_data)
    assert isinstance(updated, System)
    assert updated.version == "v2"

    # Delete
    session.delete(updated)
    session.commit()
    assert session.get(System, created.id) is None


def test_create_system_function(session):
    """Test create_system doesn't raise."""
    system = SystemCreate(version="v1", lastUpdated=datetime.now())
    result = create_system(session, system)
    assert result.id is not None


def test_read_system_function(session):
    """Test read_system returns created system."""
    system = SystemCreate(version="v1", lastUpdated=datetime.now())
    created = create_system(session, system)
    result = read_system(session, created.id)
    assert result.version == "v1"


def test_update_system_function(session):
    """Test update_system works."""
    system = SystemCreate(version="v1", lastUpdated=datetime.now())
    created = create_system(session, system)
    updated_data = SystemUpdate(version="v2", lastUpdated=datetime.now())
    result = update_system(session, created.id, updated_data)
    assert result.version == "v2"


def test_system_relationships(session):
    """No relationships to test."""
    pass