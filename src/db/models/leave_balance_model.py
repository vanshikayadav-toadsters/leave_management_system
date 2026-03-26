from sqlmodel import SQLModel, Field
from typing import Optional
import uuid 


class LeaveBalance(SQLModel, table=True):
    __tablename__ = "leave_balances"

    id: uuid.UUID = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    year: int

    total_leaves: int = Field(default=12)
    used_leaves: int = Field(default=0)