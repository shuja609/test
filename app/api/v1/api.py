from fastapi import APIRouter

api_router = APIRouter()

# Routes
from app.api.v1.endpoints import system_router
api_router.include_router(system_router.router, prefix="/system", tags=["system"])
from app.api.v1.endpoints import error_router
api_router.include_router(error_router.router, prefix="/error", tags=["error"])
from app.api.v1.endpoints import user_router
api_router.include_router(user_router.router, prefix="/user", tags=["user"])
from app.api.v1.endpoints import inventory_router
api_router.include_router(inventory_router.router, prefix="/inventory", tags=["inventory"])
from app.api.v1.endpoints import category_router
api_router.include_router(category_router.router, prefix="/category", tags=["category"])
from app.api.v1.endpoints import item_router
api_router.include_router(item_router.router, prefix="/item", tags=["item"])