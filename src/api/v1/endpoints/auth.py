from src.services.user_service import get_or_create_user
from fastapi import APIRouter, Depends
from src.db.session import get_session
from src.schemas.user_schema import LoginRequest
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.core.config import get_jwt_manager


router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/login")
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    
    jwt_manager = get_jwt_manager()
    
    user = await get_or_create_user(session, request.email)

    access_token = jwt_manager.create_access_token({"sub": user.email})
    refresh_token = jwt_manager.create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }