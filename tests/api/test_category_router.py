import pytest
import uuid
from fastapi import status
from fastapi.testclient import TestClient
from app.core.database import get_session
from app.models.category import Category
from app.api.v1.endpoints import router

# Use router in the client instance to include its routes
client = TestClient(router)

def test_create_category(client, session):
    """Test creation of a category"""
    category_data = {
        "name": "Test Category",
        "description": "This is a test category"
    }
    resp = client.post("/category/", json=category_data)
    assert resp.status_code == 201
    assert resp.json()["name"] == category_data["name"]
    assert resp.json()["description"] == category_data["description"]
    # Verify DB
    category_id = resp.json()["id"]
    assert session.get(Category, category_id) is not None

def test_get_category(client, session):
    """Test retrieval of a category by ID"""
    category = Category(name="Test Category", description="This is a test category")
    session.add(category)
    session.commit()
    session.refresh(category)
    resp = client.get(f"/category/{category.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == category.name
    assert resp.json()["description"] == category.description

def test_list_categories(client, session):
    """Test listing of all categories"""
    category1 = Category(name="Test Category 1", description="This is a test category 1")
    category2 = Category(name="Test Category 2", description="This is a test category 2")
    session.add_all([category1, category2])
    session.commit()
    session.refresh(category1)
    session.refresh(category2)
    resp = client.get("/category/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    category_ids = [c["id"] for c in resp.json()]
    assert category1.id in category_ids
    assert category2.id in category_ids

def test_update_category(client, session):
    """Test updating of a category"""
    category = Category(name="Test Category", description="This is a test category")
    session.add(category)
    session.commit()
    session.refresh(category)
    updated_category_data = {
        "name": "Updated Test Category",
        "description": "This is an updated test category"
    }
    resp = client.put(f"/category/{category.id}", json=updated_category_data)
    assert resp.status_code == 200
    assert resp.json()["name"] == updated_category_data["name"]
    assert resp.json()["description"] == updated_category_data["description"]
    # Verify DB
    updated_category = session.get(Category, category.id)
    assert updated_category.name == updated_category_data["name"]
    assert updated_category.description == updated_category_data["description"]

def test_delete_category(client, session):
    """Test deletion of a category"""
    category = Category(name="Test Category", description="This is a test category")
    session.add(category)
    session.commit()
    session.refresh(category)
    resp = client.delete(f"/category/{category.id}")
    assert resp.status_code == 204
    # Verify DB
    assert session.get(Category, category.id) is None

def test_create_category_invalid_data(client, session):
    """Test creation of a category with invalid data"""
    category_data = {
        "name": None,  # Invalid name
        "description": "This is a test category"
    }
    resp = client.post("/category/", json=category_data)
    assert resp.status_code == 422

def test_get_category_not_found(client, session):
    """Test retrieval of a non-existent category"""
    random_id = uuid.uuid4()
    resp = client.get(f"/category/{random_id}")
    assert resp.status_code == 404

def test_update_category_not_found(client, session):
    """Test updating of a non-existent category"""
    random_id = uuid.uuid4()
    updated_category_data = {
        "name": "Updated Test Category",
        "description": "This is an updated test category"
    }
    resp = client.put(f"/category/{random_id}", json=updated_category_data)
    assert resp.status_code == 404

def test_delete_category_not_found(client, session):
    """Test deletion of a non-existent category"""
    random_id = uuid.uuid4()
    resp = client.delete(f"/category/{random_id}")
    assert resp.status_code == 404