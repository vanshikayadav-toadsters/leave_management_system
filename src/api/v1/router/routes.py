from fastapi import APIRouter
from src.api.v1.endpoints import auth

from src.schemas.auth_schema import LoginRequest
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])