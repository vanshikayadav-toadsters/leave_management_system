from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
import enum

class UserRole(str, enum.Enum):
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email:str=Field(index=True, nullable=False, unique=True)
    role:UserRole=Field(default=UserRole.EMPLOYEE)
    is_active: bool = Field(default=True)