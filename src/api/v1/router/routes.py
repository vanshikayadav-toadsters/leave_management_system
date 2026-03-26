from fastapi import APIRouter
from src.api.v1.endpoints import auth
from src.api.v1.endpoints.leave_request_endpoints import router as leave_request_router

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(leave_request_router)