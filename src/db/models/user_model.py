from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
import enum

class UserRole(str, enum.Enum):
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"


class User(SQLModel, table=True):
    id:str=Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email:str=Field(index=True, nullable=False, unique=True)
    role:UserRole=Field(default=UserRole.EMPLOYEE)
    is_active: bool = Field(default=True)