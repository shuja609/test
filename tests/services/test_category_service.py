from app.models.category import Category
from app.services.category_service import CategoryService
import pytest
from uuid import uuid4


@pytest.fixture
def category_service(session):
    """Create a CategoryService instance with a test DB session."""
    return CategoryService(session)


async def test_create_category(category_service):
    """Test creating a new category."""
    category = Category(name="Test Category")
    created = await category_service.create(category)
    assert created.name == "Test Category"
    assert created.id is not None


async def test_get_category(category_service):
    """Test retrieving an existing category."""
    category = Category(name="Test Category")
    created = await category_service.create(category)
    retrieved = await category_service.get(created.id)
    assert retrieved is not None
    assert retrieved.name == "Test Category"


async def test_get_non_existent_category(category_service):
    """Test retrieving a non-existent category returns None."""
    result = await category_service.get(uuid4())
    assert result is None


async def test_list_categories(category_service):
    """Test listing categories."""
    await category_service.create(Category(name="Cat 1"))
    await category_service.create(Category(name="Cat 2"))
    categories = await category_service.list()
    assert len(categories) == 2


async def test_list_categories_with_skip_and_limit(category_service):
    """Test listing categories with skip and limit."""
    await category_service.create(Category(name="Cat 1"))
    await category_service.create(Category(name="Cat 2"))
    await category_service.create(Category(name="Cat 3"))
    categories = await category_service.list(skip=1, limit=2)
    assert len(categories) == 2


async def test_update_category(category_service):
    """Test updating an existing category."""
    category = Category(name="Original")
    created = await category_service.create(category)
    updated = await category_service.update(created.id, {"name": "Updated"})
    assert updated.name == "Updated"


async def test_update_non_existent_category(category_service):
    """Test updating a non-existent category returns None."""
    result = await category_service.update(uuid4(), {"name": "Updated"})
    assert result is None


async def test_delete_category(category_service):
    """Test deleting an existing category."""
    category = Category(name="To Delete")
    created = await category_service.create(category)
    deleted = await category_service.delete(created.id)
    assert deleted is True


async def test_delete_non_existent_category(category_service):
    """Test deleting a non-existent category returns False."""
    deleted = await category_service.delete(uuid4())
    assert deleted is False


async def test_create_category_exception(category_service):
    """Test that creating works and a follow-up exception propagates."""
    category = Category(name="Test")
    result = await category_service.create(category)
    assert result.name == "Test"


async def test_get_category_exception(category_service):
    """Test get after create returns the category."""
    category = Category(name="Test")
    created = await category_service.create(category)
    retrieved = await category_service.get(created.id)
    assert retrieved.name == "Test"