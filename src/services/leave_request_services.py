from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.leave_request_model import LeaveRequest, LeaveStatus
from src.db.models.user_model import User
from src.schemas.leave_request_schema import LeaveRequestResponse
import uuid


class LeaveRequestService:

    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def create_leave_request(self, user_id, start_date, end_date, reason):
        
        result = await self.db.execute(
            select(LeaveRequest).where(
                LeaveRequest.user_id == user_id,
                LeaveRequest.status == LeaveStatus.APPROVED,
                LeaveRequest.start_date <= end_date,
                LeaveRequest.end_date >= start_date
            )
        )
        overlapping = result.scalar_one_or_none()

        if overlapping:
            raise ValueError("You already have an overlapping approved leave")

        leave = LeaveRequest(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )

        self.db.add(leave)
        await self.db.commit()
        await self.db.refresh(leave)

        return leave

    
    async def approve_leave_request(self, leave_id: uuid.UUID):
        leave = await self.db.get(LeaveRequest, leave_id)
        if not leave:
            raise ValueError("Leave not found")

        leave.status = LeaveStatus.APPROVED
        self.db.add(leave)
        await self.db.commit()
        await self.db.refresh(leave)
        return leave

    
    async def reject_leave_request(self, leave_id: uuid.UUID):
        leave = await self.db.get(LeaveRequest, leave_id)
        if not leave:
            raise ValueError("Leave not found")

        leave.status = LeaveStatus.REJECTED
        self.db.add(leave)
        await self.db.commit()
        await self.db.refresh(leave)
        return leave

    
    async def get_my_leaves(self, user_id: uuid.UUID):
        result = await self.db.execute(
            select(LeaveRequest, User.email, User.first_name, User.last_name)
            .join(User, LeaveRequest.user_id == User.id)
            .where(LeaveRequest.user_id == user_id)
        )

        leaves = []
        for leave, email, first_name, last_name in result.all():
            leaves.append(
                LeaveRequestResponse(
                    id=leave.id,
                    user_id=leave.user_id,
                    user_email=email,
                    user_first_name=first_name,
                    user_last_name=last_name,
                    start_date=leave.start_date,
                    end_date=leave.end_date,
                    reason=leave.reason,
                    status=leave.status
                )
            )
        return leaves

    
    async def get_pending_leaves(self):
        result = await self.db.execute(
            select(LeaveRequest, User.email, User.first_name, User.last_name)
            .join(User, LeaveRequest.user_id == User.id)
            .where(LeaveRequest.status == LeaveStatus.PENDING)
        )

        leaves = []
        for leave, email, first_name, last_name in result.all():
            leaves.append(
                LeaveRequestResponse(
                    id=leave.id,
                    user_id=leave.user_id,
                    user_email=email,
                    user_first_name=first_name,
                    user_last_name=last_name,
                    start_date=leave.start_date,
                    end_date=leave.end_date,
                    reason=leave.reason,
                    status=leave.status
                )
            )
        return leaves