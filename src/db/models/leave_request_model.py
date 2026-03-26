from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
import uuid
import enum

class LeaveStatus(str, enum.Enum):
    PENDING="PENDING"
    APPROVED="APPROVED"
    REJECTED="REJECTED"

class LeaveRequest(SQLModel, table=True):
    id:uuid.UUID=Field(default_factory=uuid.uuid4, primary_key=True)
    user_id:uuid.UUID=Field(foreign_key="user.id", nullable=False)
    start_date:date=Field(nullable=False)
    end_date:date=Field(nullable=False)
    reason:Optional[str]=None
    status:LeaveStatus=Field(default=LeaveStatus.PENDING)

