import pytest
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlmodel import select


def test_user_defaults(session):
    """Test creating a User with required fields."""
    user = User(username="test", email="test@example.com", password="test123")
    session.add(user)
    session.commit()
    session.refresh(user)
    assert user.id is not None
    assert user.username == "test"
    assert user.email == "test@example.com"
    assert user.inventory is None


def test_user_with_inventory(session):
    """Test creating a User with optional inventory field."""
    user = User(username="test", email="test@example.com", password="test123", inventory="inv1")
    session.add(user)
    session.commit()
    session.refresh(user)
    assert user.inventory == "inv1"


def test_user_unique_constraint(session):
    """Test unique constraint on email."""
    user1 = User(username="test1", email="test@example.com", password="pass1")
    session.add(user1)
    session.commit()
    with pytest.raises(IntegrityError):
        user2 = User(username="test2", email="test@example.com", password="pass2")
        session.add(user2)
        session.commit()


def test_user_crud(session):
    """Test full CRUD cycle on User."""
    # Create
    user = User(username="test", email="crud@example.com", password="pass")
    session.add(user)
    session.commit()
    session.refresh(user)
    user_id = user.id

    # Read
    retrieved = session.get(User, user_id)
    assert retrieved is not None
    assert retrieved.username == "test"

    # Update
    retrieved.username = "updated"
    session.add(retrieved)
    session.commit()
    session.refresh(retrieved)
    assert retrieved.username == "updated"

    # Delete
    session.delete(retrieved)
    session.commit()
    assert session.get(User, user_id) is None


def test_user_list(session):
    """Test listing multiple users."""
    user1 = User(username="u1", email="u1@example.com", password="p1")
    user2 = User(username="u2", email="u2@example.com", password="p2")
    session.add(user1)
    session.add(user2)
    session.commit()
    results = session.exec(select(User)).all()
    assert len(results) == 2