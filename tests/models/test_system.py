# tests/test_system.py
from datetime import datetime
import pytest
from app.core.database import get_session
from app.models.system import System, SystemCreate, SystemUpdate, SystemRead, create_system, update_system, read_system

@pytest.fixture
def session():
    return get_session()

def test_system_create_defaults(session):
    system = SystemCreate(version="1.0", lastUpdated=datetime.utcnow())
    db_system = create_system(session, system)
    session.refresh(db_system)
    assert db_system.version == "1.0"
    assert db_system.lastUpdated is not None

def test_system_update_defaults(session):
    system = SystemCreate(version="1.0", lastUpdated=datetime.utcnow())
    db_system = create_system(session, system)
    updated_system = SystemUpdate(version="2.0", lastUpdated=datetime.utcnow())
    db_system = update_system(session, db_system.id, updated_system)
    session.refresh(db_system)
    assert db_system.version == "2.0"
    assert db_system.lastUpdated is not None

def test_system_create_and_read(session):
    system = SystemCreate(version="1.0", lastUpdated=datetime.utcnow())
    db_system = create_system(session, system)
    read_system_result = read_system(session, db_system.id)
    assert read_system_result.id == db_system.id
    assert read_system_result.version == db_system.version
    assert read_system_result.lastUpdated == db_system.lastUpdated

def test_system_create_duplicate(session):
    system = SystemCreate(version="1.0", lastUpdated=datetime.utcnow())
    db_system1 = create_system(session, system)
    with pytest.raises(SystemError):
        create_system(session, system)

def test_system_update_unknown(session):
    system = SystemCreate(version="1.0", lastUpdated=datetime.utcnow())
    db_system = create_system(session, system)
    updated_system = SystemUpdate(version="2.0", lastUpdated=datetime.utcnow())
    with pytest.raises(SystemError):
        update_system(session, db_system.id + 1, updated_system)

def test_system_read_unknown(session):
    with pytest.raises(SystemError):
        read_system(session, 1)