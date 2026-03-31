from app.core.database import get_session
from app.exceptions import CategoryNotFoundError
from app.services.category_service import CategoryService
from app.models.category import Category
import pytest
from uuid import uuid4

# Create category data
@pytest.fixture
def category_data():
    return Category(name="Test Category", description="Test Category Description")

# Create a category service instance with a real db session
@pytest.fixture
def category_service():
    with get_session() as session:
        yield CategoryService(session)

async def test_create_category(category_service, category_data):
    created_category = await category_service.create(category_data)
    assert created_category.name == category_data.name
    assert created_category.description == category_data.description

async def test_get_category(category_service, category_data):
    created_category = await category_service.create(category_data)
    retrieved_category = await category_service.get(created_category.id)
    assert retrieved_category.name == category_data.name
    assert retrieved_category.description == category_data.description

async def test_list_categories(category_service, category_data):
    # Create multiple categories
    for _ in range(5):
        await category_service.create(category_data)

    # Get all categories
    categories = await category_service.list()
    assert len(categories) >= 5

async def test_update_category(category_service, category_data):
    created_category = await category_service.create(category_data)
    update_data = {"name": "Updated Category", "description": "Updated Category Description"}
    updated_category = await category_service.update(created_category.id, update_data)
    assert updated_category.name == update_data["name"]
    assert updated_category.description == update_data["description"]

async def test_delete_category(category_service, category_data):
    created_category = await category_service.create(category_data)
    deleted = await category_service.delete(created_category.id)
    assert deleted is True

async def test_get_non_existent_category(category_service):
    with pytest.raises(CategoryNotFoundError):
        await category_service.get(uuid4())

async def test_update_non_existent_category(category_service):
    with pytest.raises(CategoryNotFoundError):
        await category_service.update(uuid4(), {"name": "Updated Category"})

async def test_delete_non_existent_category(category_service):
    non_existent_category_id = uuid4()
    deleted = await category_service.delete(non_existent_category_id)
    assert deleted is False

async def test_create_empty_category(category_service):
    empty_category = Category(name="", description="")
    with pytest.raises(Exception):
        await category_service.create(empty_category)

async def test_list_categories_with_skip_and_limit(category_service, category_data):
    for _ in range(10):
        await category_service.create(category_data)

    categories = await category_service.list(skip=5, limit=5)
    assert len(categories) == 5

async def test_update_category_with_empty_data(category_service, category_data):
    created_category = await category_service.create(category_data)
    update_data = {}
    updated_category = await category_service.update(created_category.id, update_data)
    assert updated_category.name == category_data.name
    assert updated_category.description == category_data.description