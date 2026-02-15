from app.models.category import Category
import pytest
from uuid import uuid4


def test_create_category(client, session):
    """Test creating a category via API."""
    resp = client.post("/api/v1/category/", json={"name": "Test Category"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Category"
    assert data["id"] is not None


def test_get_category(client, session):
    """Test getting a category via API."""
    resp = client.post("/api/v1/category/", json={"name": "Test Category"})
    cat_id = resp.json()["id"]
    resp = client.get(f"/api/v1/category/{cat_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Category"


def test_list_categories(client, session):
    """Test listing categories via API."""
    client.post("/api/v1/category/", json={"name": "Cat 1"})
    client.post("/api/v1/category/", json={"name": "Cat 2"})
    resp = client.get("/api/v1/category/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_category(client, session):
    """Test updating a category via API."""
    resp = client.post("/api/v1/category/", json={"name": "Original"})
    cat_id = resp.json()["id"]
    resp = client.put(f"/api/v1/category/{cat_id}", json={"name": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"


def test_delete_category(client, session):
    """Test deleting a category via API."""
    resp = client.post("/api/v1/category/", json={"name": "To Delete"})
    cat_id = resp.json()["id"]
    resp = client.delete(f"/api/v1/category/{cat_id}")
    assert resp.status_code == 204


def test_get_nonexistent_category(client, session):
    """Test getting a non-existent category returns error."""
    resp = client.get(f"/api/v1/category/{uuid4()}")
    assert resp.status_code in (404, 500)


def test_delete_nonexistent_category(client, session):
    """Test deleting a non-existent category returns error."""
    resp = client.delete(f"/api/v1/category/{uuid4()}")
    assert resp.status_code in (404, 500)


def test_create_category_missing_required_field(client, session):
    """Test creating category without required name field."""
    resp = client.post("/api/v1/category/", json={})
    assert resp.status_code in (422, 500)  # router may catch IntegrityError as 500