from app.core.database import get_session
from app.models.inventory import Inventory
import pytest
from sqlmodel import Session

def test_create_inventory(client, session):
    """Test creating a new inventory item."""
    inventory = {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "name": "Test Item",
        "category": "Test Category",
        "description": "Test description",
    }
    resp = client.post("/inventory/", json=inventory)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Test Item"
    # Verify DB
    assert session.get(Inventory, inventory["id"]) is not None

def test_get_inventory(client, session):
    """Test getting an existing inventory item."""
    inventory = Inventory(
        id="123e4567-e89b-12d3-a456-426655440000",
        name="Test Item",
        category="Test Category",
        description="Test description",
    )
    session.add(inventory)
    session.commit()
    resp = client.get(f"/inventory/{inventory.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Item"

def test_get_nonexistent_inventory(client, session):
    """Test getting a nonexistent inventory item."""
    resp = client.get("/inventory/123e4567-e89b-12d3-a456-426655440000")
    assert resp.status_code == 404

def test_list_inventorys(client, session):
    """Test listing inventory items."""
    inventories = [
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440000",
            name="Test Item 1",
            category="Test Category",
            description="Test description",
        ),
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440001",
            name="Test Item 2",
            category="Test Category",
            description="Test description",
        ),
    ]
    session.add_all(inventories)
    session.commit()
    resp = client.get("/inventory/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_update_inventory(client, session):
    """Test updating an existing inventory item."""
    inventory = Inventory(
        id="123e4567-e89b-12d3-a456-426655440000",
        name="Test Item",
        category="Test Category",
        description="Test description",
    )
    session.add(inventory)
    session.commit()
    updated_inventory = {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "name": "Updated Test Item",
        "category": "Updated Test Category",
        "description": "Updated Test description",
    }
    resp = client.put(f"/inventory/{inventory.id}", json=updated_inventory)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Test Item"
    # Verify DB
    assert session.get(Inventory, inventory.id).name == "Updated Test Item"

def test_update_nonexistent_inventory(client, session):
    """Test updating a nonexistent inventory item."""
    updated_inventory = {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "name": "Updated Test Item",
        "category": "Updated Test Category",
        "description": "Updated Test description",
    }
    resp = client.put("/inventory/123e4567-e89b-12d3-a456-426655440000", json=updated_inventory)
    assert resp.status_code == 404

def test_delete_inventory(client, session):
    """Test deleting an existing inventory item."""
    inventory = Inventory(
        id="123e4567-e89b-12d3-a456-426655440000",
        name="Test Item",
        category="Test Category",
        description="Test description",
    )
    session.add(inventory)
    session.commit()
    resp = client.delete(f"/inventory/{inventory.id}")
    assert resp.status_code == 204
    assert session.get(Inventory, inventory.id) is None

def test_delete_nonexistent_inventory(client, session):
    """Test deleting a nonexistent inventory item."""
    resp = client.delete("/inventory/123e4567-e89b-12d3-a456-426655440000")
    assert resp.status_code == 404

def test_get_inventory_summary(client, session):
    """Test getting the inventory summary."""
    inventories = [
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440000",
            name="Test Item 1",
            category="Test Category 1",
            description="Test description",
        ),
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440001",
            name="Test Item 2",
            category="Test Category 2",
            description="Test description",
        ),
    ]
    session.add_all(inventories)
    session.commit()
    resp = client.get("/inventory/summary")
    assert resp.status_code == 200
    assert resp.json()["total_items"] == 2
    assert resp.json()["category_count"] == 2

def test_get_items_by_category(client, session):
    """Test getting items by category."""
    inventories = [
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440000",
            name="Test Item 1",
            category="Test Category 1",
            description="Test description",
        ),
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440001",
            name="Test Item 2",
            category="Test Category 1",
            description="Test description",
        ),
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440002",
            name="Test Item 3",
            category="Test Category 2",
            description="Test description",
        ),
    ]
    session.add_all(inventories)
    session.commit()
    resp = client.get("/inventory/category/Test%20Category%201")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_search_items(client, session):
    """Test searching items."""
    inventories = [
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440000",
            name="Test Item 1",
            category="Test Category 1",
            description="Test description",
        ),
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440001",
            name="Test Item 2",
            category="Test Category 1",
            description="Test description",
        ),
        Inventory(
            id="123e4567-e89b-12d3-a456-426655440002",
            name="Test Item 3",
            category="Test Category 2",
            description="Test description",
        ),
    ]
    session.add_all(inventories)
    session.commit()
    resp = client.get("/inventory/search", params={"query": "Test Item"})
    assert resp.status_code == 200
    assert len(resp.json()) == 3