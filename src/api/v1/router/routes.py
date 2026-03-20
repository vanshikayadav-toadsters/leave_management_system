from fastapi import APIRouter

from src.api.endpoints import auth_schema
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])