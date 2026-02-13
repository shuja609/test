from typing import List, Optional, Any
from uuid import UUID
from sqlmodel import Session, select
from app.models.user import User

from app.core.database import get_session
import logging
from pydantic import EmailError, ValidationError

# Define logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, item: User) -> User:
        try:
            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail="Failed to create user")

    async def get(self, id: UUID) -> Optional[User]:
        try:
            return self.session.get(User, id)
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=404, detail="User not found")

    async def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        try:
            statement = select(User).offset(skip).limit(limit)
            return self.session.exec(statement).all()
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update(self, id: UUID, update_data: dict) -> Optional[User]:
        try:
            db_item = await self.get(id)
            if not db_item:
                return None
            
            for key, value in update_data.items():
                if hasattr(db_item, key):
                    setattr(db_item, key, value)
                else:
                    raise HTTPException(status_code=400, detail=f"Invalid field: {key}")
            
            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            return db_item
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=400, detail="Failed to update user")

    async def delete(self, id: UUID) -> bool:
        try:
            db_item = await self.get(id)
            if not db_item:
                return False
            
            self.session.delete(db_item)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(status_code=404, detail="User not found")

    async def validate_input(self, obj: dict):
        try:
            user = User.from_orm(obj)
            return user
        except (ValidationError, EmailError) as e:
            raise HTTPException(status_code=400, detail=str(e))

Note that I've added error handling to the existing methods, as well as a new `validate_input` method to validate the input data before creating a new user. This `validate_input` method uses Pydantic's built-in `from_orm` method to validate the input dictionary against the `User` model.

Also, I've added a `try-except` block in the `update` method to catch any HTTP exceptions that might be raised when trying to update an invalid field.

Additionally, I've added a basic logging configuration to log any errors that occur during the execution of the methods.

You can use the `validate_input` method like this:

async def create_user(self, item: dict):
    validated_item = await self.validate_input(item)
    return await self.create(validated_item)

This will ensure that the input data is validated before creating a new user.