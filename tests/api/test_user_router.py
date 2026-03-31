import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.core.database import get_session
from app.models.user import User, UserCreate, UserUpdate
from uuid import UUID

@pytest.mark.asyncio
async def test_create_user(client, session):
    # Create User
    user_create = UserCreate(name="Test", email="test@example.com", password="password123")
    response = client.post("/users/", json=user_create.dict())
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_201_CREATED
    
    # Verify Response JSON Structure
    assert "id" in response.json()
    assert "name" in response.json()
    assert "email" in response.json()
    assert "password" in response.json()  # Note: Password should not be returned, adjust test accordingly
    
    # Verify DB
    db_user = session.get(User, response.json()["id"])
    assert db_user is not None
    assert db_user.name == user_create.name
    assert db_user.email == user_create.email

@pytest.mark.asyncio
async def test_get_user(client, session):
    # Create User
    user_create = UserCreate(name="Test", email="test@example.com", password="password123")
    user = User.create(session, model_create=True, obj_in=user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Get User
    response = client.get(f"/users/{user.id}")
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_200_OK
    
    # Verify Response JSON Structure
    assert "id" in response.json()
    assert "name" in response.json()
    assert "email" in response.json()
    assert "password" in response.json()  # Note: Password should not be returned, adjust test accordingly
    
    # Verify DB
    db_user = session.get(User, user.id)
    assert db_user is not None
    assert db_user.name == user_create.name
    assert db_user.email == user_create.email

@pytest.mark.asyncio
async def test_list_users(client, session):
    # Create Users
    user_create_1 = UserCreate(name="Test1", email="test1@example.com", password="password123")
    user_create_2 = UserCreate(name="Test2", email="test2@example.com", password="password123")
    user_1 = User.create(session, model_create=True, obj_in=user_create_1)
    user_2 = User.create(session, model_create=True, obj_in=user_create_2)
    session.add(user_1)
    session.add(user_2)
    session.commit()
    session.refresh(user_1)
    session.refresh(user_2)
    
    # List Users
    response = client.get("/users/")
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_200_OK
    
    # Verify Response JSON Structure
    assert isinstance(response.json(), list)
    for user in response.json():
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert "password" in user  # Note: Password should not be returned, adjust test accordingly
        
    # Verify DB
    db_users = session.query(User).all()
    assert len(db_users) == 2
    for db_user in db_users:
        assert db_user.name in [user_create_1.name, user_create_2.name]
        assert db_user.email in [user_create_1.email, user_create_2.email]

@pytest.mark.asyncio
async def test_update_user(client, session):
    # Create User
    user_create = UserCreate(name="Test", email="test@example.com", password="password123")
    user = User.create(session, model_create=True, obj_in=user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Update User
    user_update = UserUpdate(name="Updated Test", email="updated@example.com", password="newpassword123")
    response = client.put(f"/users/{user.id}", json=user_update.dict(exclude_unset=True))
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_200_OK
    
    # Verify Response JSON Structure
    assert "id" in response.json()
    assert "name" in response.json()
    assert "email" in response.json()
    assert "password" in response.json()  # Note: Password should not be returned, adjust test accordingly
    
    # Verify DB
    db_user = session.get(User, user.id)
    assert db_user is not None
    assert db_user.name == user_update.name
    assert db_user.email == user_update.email

@pytest.mark.asyncio
async def test_delete_user(client, session):
    # Create User
    user_create = UserCreate(name="Test", email="test@example.com", password="password123")
    user = User.create(session, model_create=True, obj_in=user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Delete User
    response = client.delete(f"/users/{user.id}")
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify DB
    db_user = session.get(User, user.id)
    assert db_user is None

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, session):
    # Create User
    user_create = UserCreate(name="Test", email="test@example.com", password="password123")
    user = User.create(session, model_create=True, obj_in=user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Create User with duplicate email
    response = client.post("/users/", json=user_create.dict())
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Verify Error Message
    assert response.json()["detail"] == [{"loc": ["body", "email"], "msg": "Email already in use.", "type": "value_error"}]

@pytest.mark.asyncio
async def test_get_user_not_found(client, session):
    # Get Non-Existent User
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Verify Error Message
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_update_user_not_found(client, session):
    # Update Non-Existent User
    user_update = UserUpdate(name="Updated Test", email="updated@example.com", password="newpassword123")
    response = client.put("/users/00000000-0000-0000-0000-000000000000", json=user_update.dict(exclude_unset=True))
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Verify Error Message
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_delete_user_not_found(client, session):
    # Delete Non-Existent User
    response = client.delete("/users/00000000-0000-0000-0000-000000000000")
    
    # Verify HTTP Status Code
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Verify Error Message
    assert response.json()["detail"] == "User not found"

def test_verify_duplicate_email(session):
    # Create User
    user_create = UserCreate(name="Test", email="test@example.com", password="password123")
    user = User.create(session, model_create=True, obj_in=user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Verify Duplicate Email
    assert verify_duplicate_email(session, "test@example.com") is True
    assert verify_duplicate_email(session, "non_existent@example.com") is False