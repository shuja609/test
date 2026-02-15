# tests/models/test_error.py
from app.models.error import Error, ErrorModel
import pytest


def test_error_defaults(session):
    """Test creating Error with required fields"""
    error = Error(message="Test error", code=500)
    session.add(error)
    session.commit()
    session.refresh(error)
    assert error.id is not None
    assert error.message == "Test error"
    assert error.code == 500


def test_error_crud(session):
    """Test full CRUD on Error model"""
    # Create
    error = Error(message="Test error", code=500)
    session.add(error)
    session.commit()
    session.refresh(error)
    assert error.id is not None

    # Read
    retrieved = session.get(Error, error.id)
    assert retrieved is not None
    assert retrieved.message == "Test error"
    assert retrieved.code == 500

    # Update
    error.message = "Updated error"
    session.add(error)
    session.commit()
    session.refresh(error)
    assert error.message == "Updated error"

    # Delete
    session.delete(error)
    session.commit()
    assert session.get(Error, error.id) is None


def test_error_model_validation():
    """Test ErrorModel pydantic schema"""
    model = ErrorModel(detail="Something went wrong")
    assert model.detail == "Something went wrong"


def test_multiple_errors(session):
    """Test creating multiple errors"""
    e1 = Error(message="Error 1", code=400)
    e2 = Error(message="Error 2", code=500)
    session.add(e1)
    session.add(e2)
    session.commit()
    from sqlmodel import select
    results = session.exec(select(Error)).all()
    assert len(results) == 2


def test_relationships(session):
    """No relationships defined in the Error model"""
    pass