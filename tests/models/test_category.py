# tests/test_category.py
from app.core.database import get_session
from app.models.category import Category
from app.exceptions import BaseException
import pytest

@pytest.fixture
def session():
    yield get_session()

def test_category_defaults(session):
    category = Category(name="toiletries")
    session.add(category)
    session.commit()
    session.refresh(category)
    assert category.id is not None
    assert category.id != ""
    assert category.name == "toiletries"

def test_create_category(session):
    category = Category.create_category(name="electronics")
    session.add(category)
    session.commit()
    session.refresh(category)
    assert category.name == "electronics"

def test_create_category_validation(session):
    with pytest.raises(BaseException):
        Category.create_category(name=None)

def test_create_duplicate_category(session):
    category1 = Category.create_category(name="toiletries")
    session.add(category1)
    session.commit()
    session.refresh(category1)
    with pytest.raises(BaseException):
        category2 = Category.create_category(name="toiletries")
        session.add(category2)
        session.commit()

def test_get_categories(session):
    categories = Category.get_categories()
    assert categories == ["toiletries", "electronics", "clothing"]

def test_create_update_category(session):
    category = Category.create_category(name="clothing")
    session.add(category)
    session.commit()
    session.refresh(category)
    category.name = "new_clothing"
    session.add(category)
    session.commit()
    session.refresh(category)
    assert category.name == "new_clothing"

def test_delete_category(session):
    category = Category.create_category(name="toiletries")
    session.add(category)
    session.commit()
    session.refresh(category)
    session.delete(category)
    session.commit()
    assert session.query(Category).filter(Category.name == "toiletries").first() is None

def test_str_representation(session):
    category = Category.create_category(name="electronics")
    session.add(category)
    session.commit()
    session.refresh(category)
    assert str(category) == "electronics"

def test_repr_representation(session):
    category = Category.create_category(name="electronics")
    session.add(category)
    session.commit()
    session.refresh(category)
    assert repr(category) == f"Category(name='{category.name}')"