# tests/test_error.py
from app.models.error import Error, create_error, get_error_by_message
from app.core.database import get_session
from fastapi import HTTPException
import pytest

@pytest.fixture
def session():
    with get_session() as session:
        yield session

def test_error_create(session):
    # Test creating a new error instance
    error = Error(message="Test error", code=500)
    session.add(error)
    session.commit()
    assert error.id is not None

def test_error_get_by_message(session):
    # Test retrieving an error instance by message
    error = create_error("Test error", 500)
    retrieved_error = get_error_by_message("Test error")
    assert retrieved_error.message == "Test error"

def test_error_field_validation():
    # Test field validation (length and regex)
    with pytest.raises(ValueError):
        Error(message="a" * 1001, code=500)  # max_length exceeded

def test_error_table_constraint_unique(session):
    # Test unique constraint (duplicate error message)
    create_error("Test error", 500)
    with pytest.raises(Exception):
        create_error("Test error", 500)  # duplicate error message

def test_error_defaults(session):
    # Test default values
    error = Error(message="Test error")
    session.add(error)
    session.commit()
    session.refresh(error)
    assert error.code is None  # default

def test_error_crud(session):
    # Test basic CRUD operations
    error = Error(message="Test error", code=500)
    session.add(error)
    session.commit()

    # Read
    retrieved_error = session.query(Error).first()
    assert retrieved_error.message == "Test error"

    # Update
    error.message = "Updated error"
    session.commit()
    retrieved_error = session.query(Error).first()
    assert retrieved_error.message == "Updated error"

    # Delete
    session.delete(retrieved_error)
    session.commit()
    assert session.query(Error).first() is None

def test_handle_validation_error():
    # Test handling validation error
    try:
        ErrorModel(detail="")
    except ValidationError as exc:
        error = Error(message="Invalid error model", code=422)
        error_model = ErrorModel(detail=error.message)
        assert error_model.detail == error.message

def test_handle_duplicate_error(session):
    # Test handling duplicate error
    create_error("Test error", 500)
    try:
        handle_duplicate_error("Test error", 500)
    except HTTPException as exc:
        assert exc.status_code == 500
        assert exc.detail == "Internal Server Error"

def test_create_error_exception():
    # Test create error exception
    with pytest.raises(HTTPException):
        create_error("", 500)  # invalid message

def test_get_error_by_message_exception():
    # Test get error by message exception
    with pytest.raises(HTTPException):
        get_error_by_message("")