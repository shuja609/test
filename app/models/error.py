# app/models/error.py
from typing import Optional
from sqlmodel import Field, SQLModel, table
import logging
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException
from app.core.database import get_session

logging.basicConfig(level=logging.INFO)

class Error(SQLModel, table=True):
    """
    Error model.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    code: int

class ErrorModel(BaseModel):
    """
    Error model for validation.
    """
    detail: str

def create_error(message: str, code: int) -> Error:
    """
    Creates a new error instance.
    
    Args:
        message (str): Error message.
        code (int): Error code.
    
    Returns:
        Error: New error instance.
    """
    try:
        with get_session() as session:
            error = Error(message=message, code=code)
            session.add(error)
            session.commit()
            return error
    except Exception as e:
        logging.error(f"Error creating error instance: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_error_by_message(message: str) -> Error:
    """
    Retrieves an error instance by message.
    
    Args:
        message (str): Error message.
    
    Returns:
        Error: Error instance if found, None otherwise.
    """
    try:
        with get_session() as session:
            return session.query(Error).filter(Error.message == message).first()
    except Exception as e:
        logging.error(f"Error retrieving error instance: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def handle_validation_error(exc: ValidationError) -> ErrorModel:
    """
    Handles validation errors and creates an error instance.
    
    Args:
        exc (ValidationError): Validation error.
    
    Returns:
        ErrorModel: Error model with validation error details.
    """
    error_messages = exc.errors()
    messages = [f"{key}: {error['msg']}" for key, error in error_messages.items()]
    message = ", ".join(messages)
    code = 422  # HTTP 422 Unprocessable Entity
    error = create_error(message, code)
    return ErrorModel(detail=error.message)

def handle_duplicate_error(message: str, code: int) -> ErrorModel:
    """
    Handles duplicate errors and creates an error instance.
    
    Args:
        message (str): Error message.
        code (int): Error code.
    
    Returns:
        ErrorModel: Error model with duplicate error details.
    """
    error = get_error_by_message(message)
    if error:
        return ErrorModel(detail=f"Item with message '{message}' already exists.")
    error = create_error(message, code)
    return ErrorModel(detail=error.message)
