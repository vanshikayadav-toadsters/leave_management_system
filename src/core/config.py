from src.core.settings import settings
from src.core.security import JWTManager


def get_jwt_manager() ->  JWTManager:
    return JWTManager(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_expiry_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_expiry_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )