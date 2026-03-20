from pydantic import BaseModel , EmailStr , field_validator
from src.core.settings import settings


class LoginRequest(BaseModel):
    email:EmailStr

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: EmailStr):
        domain = value.split("@")[-1]

        allowed_domains=settings.WHITELISTED_DOMAINS.split(",")

        if domain not in allowed_domains:
            raise ValueError("Email not allowed")

        return value

        