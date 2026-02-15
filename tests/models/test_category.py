from app.models.category import Category
import pytest
from sqlalchemy.exc import IntegrityError


def test_create_category_defaults(session):
    """Test default values for Category"""
    category = Category(name="test")
    session.add(category)
    session.commit()
    session.refresh(category)
    assert category.id is not None
    assert category.name == "test"
    assert category.description is None
    assert category.parent_id is None


def test_create_category_with_all_fields(session):
    """Test creating Category with all fields"""
    category = Category(name="test", description="desc", parent_id=None)
    session.add(category)
    session.commit()
    session.refresh(category)
    assert category.name == "test"
    assert category.description == "desc"


def test_update_category(session):
    """Test updating a Category instance"""
    category = Category(name="test")
    session.add(category)
    session.commit()
    session.refresh(category)
    category.name = "updated"
    session.commit()
    session.refresh(category)
    assert category.name == "updated"


def test_delete_category(session):
    """Test deleting a Category instance"""
    category = Category(name="test")
    session.add(category)
    session.commit()
    session.delete(category)
    session.commit()
    result = session.get(Category, category.id)
    assert result is None


def test_category_crud(session):
    """Test full CRUD cycle"""
    # Create
    category = Category(name="crud_test")
    session.add(category)
    session.commit()
    session.refresh(category)
    cat_id = category.id

    # Read
    retrieved = session.get(Category, cat_id)
    assert retrieved is not None
    assert retrieved.name == "crud_test"

    # Update
    retrieved.description = "updated desc"
    session.add(retrieved)
    session.commit()
    session.refresh(retrieved)
    assert retrieved.description == "updated desc"

    # Delete
    session.delete(retrieved)
    session.commit()
    assert session.get(Category, cat_id) is None


def test_multiple_categories(session):
    """Test creating multiple categories"""
    cat1 = Category(name="cat1")
    cat2 = Category(name="cat2")
    session.add(cat1)
    session.add(cat2)
    session.commit()
    from sqlmodel import select
    results = session.exec(select(Category)).all()
    assert len(results) == 2