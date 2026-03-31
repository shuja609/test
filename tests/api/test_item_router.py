import pytest
from fastapi import status
from app.exceptions import InvalidCategoryError, ItemNotFoundError
from app.models.item import Item, CATEGORIES
from uuid import uuid4

def test_create_item(client, session):
    item_data = {"name": "Test Item", "category": CATEGORIES[0]}
    resp = client.post("/items/", json=item_data)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Test Item"
    assert resp.json()["category"] == CATEGORIES[0]
    # Verify DB
    item_id = resp.json()["id"]
    assert session.get(Item, item_id) is not None

def test_create_item_invalid_category(client, session):
    item_data = {"name": "Test Item", "category": "Invalid Category"}
    resp = client.post("/items/", json=item_data)
    assert resp.status_code == 500
    assert resp.json()["detail"] == "Failed to create item"

def test_get_item(client, session):
    item_data = {"name": "Test Item", "category": CATEGORIES[0]}
    item_id = session.add(Item(**item_data))
    session.commit()
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Item"
    assert resp.json()["category"] == CATEGORIES[0]

def test_get_item_not_found(client, session):
    resp = client.get(f"/items/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Item not found"

def test_list_items(client, session):
    for _ in range(10):
        item_data = {"name": f"Test Item {_}", "category": CATEGORIES[0]}
        session.add(Item(**item_data))
    session.commit()
    resp = client.get("/items/")
    assert resp.status_code == 200
    assert len(resp.json()) == 10

def test_update_item(client, session):
    item_data = {"name": "Test Item", "category": CATEGORIES[0]}
    item_id = session.add(Item(**item_data))
    session.commit()
    update_data = {"name": "Updated Item"}
    resp = client.put(f"/items/{item_id}", json=update_data)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Item"
    # Verify DB
    assert session.get(Item, item_id).name == "Updated Item"

def test_update_item_not_found(client, session):
    update_data = {"name": "Updated Item"}
    resp = client.put(f"/items/{uuid4()}", json=update_data)
    assert resp.status_code == 500
    assert resp.json()["detail"] == "Failed to update item"

def test_delete_item(client, session):
    item_data = {"name": "Test Item", "category": CATEGORIES[0]}
    item_id = session.add(Item(**item_data))
    session.commit()
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 204
    # Verify DB
    assert session.get(Item, item_id) is None

def test_delete_item_not_found(client, session):
    resp = client.delete(f"/items/{uuid4()}")
    assert resp.status_code == 500
    assert resp.json()["detail"] == "Failed to delete item"

def test_get_summary(client, session):
    for _ in range(10):
        item_data = {"name": f"Test Item {_}", "category": CATEGORIES[0]}
        session.add(Item(**item_data))
    session.commit()
    resp = client.get("/items/summary")
    assert resp.status_code == 200
    assert len(resp.json()) == 10

def test_get_categories(client, session):
    resp = client.get("/items/categories")
    assert resp.status_code == 200
    assert resp.json() == CATEGORIES

def test_filter_items(client, session):
    for i in range(10):
        item_data = {"name": f"Test Item {i}", "category": CATEGORIES[i % 2]}
        session.add(Item(**item_data))
    session.commit()
    resp = client.get("/items/filter", params={"name": "Item 1"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    resp = client.get("/items/filter", params={"category": CATEGORIES[0]})
    assert resp.status_code == 200
    assert len(resp.json()) == 5