from typing import List, Optional, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import EmailError, ValidationError

from app.core.database import get_session
from app.models.category import Category
from app.models.inventory import Inventory

import logging
logger = logging.getLogger(__name__)

class User(SQLModel, table=True):
    """
    User model.
    """
    id: str
    username: str
    email: str = Field(unique=True, index=True)
    password: str
    inventory: str

    class Config:
        anystrNormalization = True
        validate_assignment = True

    def __init__(self, id: str, username: str, email: str, password: str, inventory: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.inventory = inventory

    def is_email_valid(self):
        try:
            return EmailError(self.email).as_str() is None
        except EmailError as e:
            return False

    def is_unique(self, existing_users: List['User']):
        return not any(user.email == self.email for user in existing_users)

def validate_user_data(email: str, username: str) -> Optional[dict]:
    errors = {}
    if not email or not User.is_email_valid(email):
        errors['email'] = ['Invalid email']
    if len(username) < 3:
        errors['username'] = ['Username must be at least 3 characters long']
    return errors

def validate_user(user: User) -> str:
    errors = validate_user_data(user.email, user.username)
    if user.email and not user.is_unique([User(id='id1', username='user1', email=user.email, password='pw1', inventory='it1')]):
        errors['email'] = ['Email already exists']
    if errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errors)
    return user.id

class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, user: User) -> User:
        try:
            validated_user_id = validate_user(user)
            db_user = User(
                id=validated_user_id,
                username=user.username,
                email=user.email,
                password=user.password,
                inventory=user.inventory
            )
            self.session.add(db_user)
            await self.session.commit()
            return db_user
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
