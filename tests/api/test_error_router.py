from uuid import uuid4
from fastapi import status
from app.core.database import get_session
from app.models.error import Error
import pytest

# Create a test error item
def create_test_error():
    return Error(id=uuid4(), name="Test Error")

# Test create error
def test_create_error(client, session):
    # Create a test error
    test_error = create_test_error()
    # Post the error to the API
    resp = client.post("/errors/", json=test_error.dict())
    # Verify the response status code
    assert resp.status_code == status.HTTP_201_CREATED
    # Verify the response JSON structure
    assert resp.json()["name"] == test_error.name
    # Verify the error was created in the database
    assert session.get(Error, resp.json()["id"]) is not None

# Test get error
def test_get_error(client, session):
    # Create a test error
    test_error = create_test_error()
    session.add(test_error)
    session.commit()
    # Get the error from the API
    resp = client.get(f"/errors/{test_error.id}")
    # Verify the response status code
    assert resp.status_code == status.HTTP_200_OK
    # Verify the response JSON structure
    assert resp.json()["name"] == test_error.name

# Test list errors
def test_list_errors(client, session):
    # Create a few test errors
    for _ in range(5):
        test_error = create_test_error()
        session.add(test_error)
    session.commit()
    # List the errors from the API
    resp = client.get("/errors/")
    # Verify the response status code
    assert resp.status_code == status.HTTP_200_OK
    # Verify the response JSON structure
    assert len(resp.json()) == 5

# Test update error
def test_update_error(client, session):
    # Create a test error
    test_error = create_test_error()
    session.add(test_error)
    session.commit()
    # Update the error
    updated_test_error = create_test_error()
    updated_test_error.id = test_error.id
    # Put the updated error to the API
    resp = client.put(f"/errors/{test_error.id}", json=updated_test_error.dict())
    # Verify the response status code
    assert resp.status_code == status.HTTP_200_OK
    # Verify the response JSON structure
    assert resp.json()["name"] == updated_test_error.name
    # Verify the error was updated in the database
    assert session.get(Error, test_error.id).name == updated_test_error.name

# Test delete error
def test_delete_error(client, session):
    # Create a test error
    test_error = create_test_error()
    session.add(test_error)
    session.commit()
    # Delete the error from the API
    resp = client.delete(f"/errors/{test_error.id}")
    # Verify the response status code
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    # Verify the error was deleted from the database
    assert session.get(Error, test_error.id) is None

# Test get error with 404
def test_get_error_404(client, session):
    # Get a non-existent error from the API
    resp = client.get(f"/errors/{uuid4()}")
    # Verify the response status code
    assert resp.status_code == status.HTTP_404_NOT_FOUND

# Test update error with 404
def test_update_error_404(client, session):
    # Create a test error
    test_error = create_test_error()
    # Put the updated error to the API with a non-existent id
    resp = client.put(f"/errors/{uuid4()}", json=test_error.dict())
    # Verify the response status code
    assert resp.status_code == status.HTTP_404_NOT_FOUND

# Test delete error with 404
def test_delete_error_404(client, session):
    # Delete a non-existent error from the API
    resp = client.delete(f"/errors/{uuid4()}")
    # Verify the response status code
    assert resp.status_code == status.HTTP_404_NOT_FOUND