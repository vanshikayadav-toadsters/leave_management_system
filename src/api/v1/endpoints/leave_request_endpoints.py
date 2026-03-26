from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from src.schemas.leave_request_schema import (
    LeaveRequestCreate,
    LeaveRequestResponse
)
from src.services.leave_request_services import LeaveRequestService
from src.utils.auth import get_current_user
from src.db.session import get_session
from src.db.models.user_model import UserRole


router = APIRouter(prefix="/leaves", tags=["Leave Requests"])



@router.post("/", response_model=LeaveRequestResponse)
async def apply_leave(
    leave: LeaveRequestCreate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    service = LeaveRequestService(session)

    try:
        return await service.create_leave_request(
            user_id=current_user.id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            reason=leave.reason
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.patch("/{leave_id}/approve", response_model=LeaveRequestResponse)
async def approve_leave(
    leave_id: uuid.UUID,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    if current_user.role != UserRole.HR:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = LeaveRequestService(session)

    try:
        return await service.approve_leave_request(leave_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.patch("/{leave_id}/reject", response_model=LeaveRequestResponse)
async def reject_leave(
    leave_id: uuid.UUID,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    if current_user.role != UserRole.HR:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = LeaveRequestService(session)

    try:
        return await service.reject_leave_request(leave_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.get("/my", response_model=List[LeaveRequestResponse])
async def get_my_leaves(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    service = LeaveRequestService(session)

    return await service.get_my_leaves(current_user.id)



@router.get("/pending", response_model=List[LeaveRequestResponse])
async def get_pending_leaves(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    if current_user.role != UserRole.HR:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = LeaveRequestService(session)

    return await service.get_pending_leaves()