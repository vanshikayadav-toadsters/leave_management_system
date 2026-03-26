from pydantic import BaseModel
from datetime import date
from typing import Optional
from src.db.models.leave_request_model import LeaveStatus
from uuid import UUID

class LeaveRequestCreate(BaseModel):
    start_date:date
    end_date:date
    reason:Optional[str]=None

    @classmethod
    def validate_dates(cls, values):
        start=values.get("start date")
        end = values.get("end_date")
        if end < start:
            raise ValueError("end_date cannot be before start_date")
        return values


class LeaveRequestResponse(BaseModel):
    id:UUID
    user_id:UUID
    user_email: str         
    user_first_name: Optional[str]  
    user_last_name: Optional[str]
    start_date:date
    end_date:date
    reason:Optional[str]
    status:LeaveStatus

    model_config = {
    "from_attributes": True
}