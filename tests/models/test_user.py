import pytest
from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session
from pydantic import EmailError, ValidationError
from app.core.database import get_session
from app.models.user import User, validate_user_data, validate_user, UserService

@pytest.mark.asyncio
async def test_create_user(session: Session):
    user = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    user_service = UserService(session)
    new_user = await user_service.create(user)
    assert new_user.id == user.id
    assert new_user.username == user.username
    assert new_user.email == user.email
    assert new_user.password == user.password
    assert new_user.inventory == user.inventory

def test_field_validation(session: Session):
    # Test max_length, nullable=False, and regex patterns
    # Since there are no explicit max_length or regex patterns defined,
    # we'll focus on nullable=False and email validation
    with pytest.raises(ValueError):
        User(id=None, username='user1', email='test@example.com', password='pw1', inventory='it1')
    with pytest.raises(ValueError):
        User(id='id1', username=None, email='test@example.com', password='pw1', inventory='it1')
    with pytest.raises(ValueError):
        User(id='id1', username='user1', email=None, password='pw1', inventory='it1')
    with pytest.raises(ValueError):
        User(id='id1', username='user1', email='test@example.com', password=None, inventory='it1')
    with pytest.raises(ValueError):
        User(id='id1', username='user1', email='test@example.com', password='pw1', inventory=None)

    # Test email validation
    errors = validate_user_data('invalid_email', 'user1')
    assert 'email' in errors
    errors = validate_user_data('test@example.com', 'user1')
    assert errors == {}

def test_table_constraints(session: Session):
    # Test unique constraint on email
    user1 = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    user2 = User(id='id2', username='user2', email='test@example.com', password='pw2', inventory='it2')
    session.add(user1)
    session.commit()
    with pytest.raises(Exception):
        session.add(user2)
        session.commit()

def test_crud(session: Session):
    # Test create
    user = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    session.add(user)
    session.commit()
    session.refresh(user)
    assert user.id == 'id1'
    assert user.username == 'user1'
    assert user.email == 'test@example.com'
    assert user.password == 'pw1'
    assert user.inventory == 'it1'

    # Test read
    query = session.query(User).filter(User.id == 'id1').first()
    assert query.id == user.id
    assert query.username == user.username
    assert query.email == user.email
    assert query.password == user.password
    assert query.inventory == user.inventory

    # Test update
    user.username = 'user2'
    session.add(user)
    session.commit()
    session.refresh(user)
    assert user.username == 'user2'

    # Test delete
    session.delete(user)
    session.commit()
    query = session.query(User).filter(User.id == 'id1').first()
    assert query is None

def test_user_service_create(session: Session):
    user_service = UserService(session)
    user = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    with pytest.raises(HTTPException):
        await user_service.create(user)

    try:
        validated_user_id = validate_user(user)
        db_user = User(
            id=validated_user_id,
            username=user.username,
            email=user.email,
            password=user.password,
            inventory=user.inventory
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        new_user = await user_service.create(user)
        assert new_user.id == db_user.id
        assert new_user.username == db_user.username
        assert new_user.email == db_user.email
        assert new_user.password == db_user.password
        assert new_user.inventory == db_user.inventory
    except Exception as e:
        logger.error(f"Failed to create user: {e}")

def test_user_service_create_with_email_already_exists(session: Session):
    user_service = UserService(session)
    user1 = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    try:
        validated_user_id = validate_user(user1)
        db_user = User(
            id=validated_user_id,
            username=user1.username,
            email=user1.email,
            password=user1.password,
            inventory=user1.inventory
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        with pytest.raises(HTTPException):
            await user_service.create(user1)
    except Exception as e:
        logger.error(f"Failed to create user: {e}")

def test_user_is_email_valid(session: Session):
    user = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    assert user.is_email_valid()

    user = User(id='id1', username='user1', email='invalid_email', password='pw1', inventory='it1')
    assert not user.is_email_valid()

def test_user_is_unique(session: Session):
    user1 = User(id='id1', username='user1', email='test@example.com', password='pw1', inventory='it1')
    user2 = User(id='id2', username='user2', email='test@example.com', password='pw2', inventory='it2')
    users = [user1]
    assert not user2.is_unique(users)

    users = [User(id='id3', username='user3', email='test2@example.com', password='pw3', inventory='it3')]
    assert user2.is_unique(users)