from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from api.v1.officers.schemas import Officer, OfficerCreate, OfficerUpdate
from api.v1.auth.auth import get_current_user
from database.session import get_session

router = APIRouter(tags=["Officer"])


@router.get("/", response_model=List[Officer])
async def get_officers(session: AsyncSession = Depends(get_session)):
    officers = await crud.get_officers(session=session)
    return officers


@router.post("/", response_model=Officer)
async def create_officer(officer: OfficerCreate,
                         session: AsyncSession = Depends(get_session),
                         current_user: dict = Depends(get_current_user)
                         ):
    return await crud.create_officer(session=session, officer=officer)


@router.get("/{officer_id}", response_model=dict)
async def get_officer_by_id(officer_id: int, session: AsyncSession = Depends(get_session)):
    officer = await crud.get_officer_by_id(session=session, officer_id=officer_id)

    if officer:
        return officer

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Officer {officer_id} not found"
    )


@router.put("/{officer_id}", response_model=OfficerUpdate)
async def update_officer(
        officer_id: int,
        officer_update: OfficerUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: dict = Depends(get_current_user)
):
    updated_officer = await crud.update_officer(session, officer_id, officer_update)

    if not updated_officer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found"
        )
    return updated_officer


@router.delete("/{officer_id}", response_model=dict)
async def delete_officer(officer_id: int,
                         session: AsyncSession = Depends(get_session),
                         current_user: dict = Depends(get_current_user)
                         ):
    success = await crud.delete_officer(session=session, officer_id=officer_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found"
        )

    return {"detail": f"Officer {officer_id} deleted successfully"}
