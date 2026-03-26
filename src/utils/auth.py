from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.session import get_session
from src.db.models.user_model import User
from src.core.config import get_jwt_manager
from fastapi.security import OAuth2PasswordBearer

security = HTTPBearer()

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security),
    session:AsyncSession=Depends(get_session)
):
    
    token=credentials.credentials
    
    jwt_manager=get_jwt_manager()

    try:
        payload=jwt_manager.decode_token(token)
        

        email=payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid Token")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user