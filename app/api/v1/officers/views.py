from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from . import crud
from app.api.v1.officers.schemas import Officer, OfficerCreate, OfficerUpdate
from app.api.v1.auth.auth import get_current_user
from app.database.session import get_session
from app.api.v1.departments.crud import get_department_by_id


router = APIRouter(tags=["Officer"])


@router.get("/", response_model=List[Officer])
async def get_officers(session: AsyncSession = Depends(get_session)):

    try:
        officers = await crud.get_officers(session=session)
        return officers
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.post("/", response_model=Officer)
async def create_officer(
        officer: OfficerCreate,
        session: AsyncSession = Depends(get_session),
        current_user: dict = Depends(get_current_user)
):
    if officer.department_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department ID is required"
        )

    try:

        department = await get_department_by_id(session, officer.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department with ID {officer.department_id} does not exist"
            )

        return await crud.create_officer(session=session, officer=officer)

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error This mail already exists"
        )


@router.get("/{officer_id}/", response_model=dict)
async def get_officer_by_id(officer_id: int,
                            session: AsyncSession = Depends(get_session)
                            ):
    try:
        officer = await crud.get_officer_by_id(session=session, officer_id=officer_id)
        if officer:
            return officer
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.put("/{officer_id}/", response_model=OfficerUpdate)
async def update_officer(
        officer_id: int,
        officer_update: OfficerUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: dict = Depends(get_current_user)
):

    try:
        updated_officer = await crud.update_officer(session, officer_id, officer_update)
        if not updated_officer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Officer {officer_id} not found"
            )
        return updated_officer
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )


@router.delete("/{officer_id}/", response_model=dict)
async def delete_officer(
        officer_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: dict = Depends(get_current_user)
):

    try:
        success = await crud.delete_officer(session=session, officer_id=officer_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Officer {officer_id} not found"
            )
        return {"detail": f"Officer {officer_id} deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
