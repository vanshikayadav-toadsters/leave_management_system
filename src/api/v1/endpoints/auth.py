from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.schemas.auth_schema import LoginRequest
from src.db.model.user_model import User
from src.db.session import get_session
from src.core.config import get_jwt_manager

router = APIRouter()

@router.post("/login")
async def login(
    request: LoginRequest,
    session:AsyncSession=Depends(get_session)
):

    jwt_manager = get_jwt_manager()
     result = await session.execute(
        select(User).where(User.email == request.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        user=User(email=request.email)
        session.add(user)
        await session.commit()
        await session.refresh(user)


    access_token = jwt_manager.create_access_token({"sub": user.email})
    refresh_token = jwt_manager.create_refresh_token({"sub": user.email})

    return{
        "access_token":access_token,
        "refresh_token": refresh_token,
        "token_type":"bearer"
    }

