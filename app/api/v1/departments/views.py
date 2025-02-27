from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.departments import crud
from app.api.v1.departments.schemas import Department, DepartmentCreate, DepartmentUpdate
from app.api.v1.auth.auth import get_current_user
from app.database.session import get_session

router = APIRouter(tags=["Departments"])


@router.get("/", response_model=List[Department])
async def get_departments(session: AsyncSession = Depends(get_session)):
    return await crud.get_departments(session=session)


@router.post("/", response_model=Department)
async def create_department(department: DepartmentCreate,
                            session: AsyncSession = Depends(get_session),
                            current_user: dict = Depends(get_current_user)
                            ):

    return await crud.create_department(session=session, department=department)


@router.get("/{department_id}/", response_model=Department)
async def get_department_by_id(department_id: int,
                               session: AsyncSession = Depends(get_session)
                               ):

    department = await crud.get_department_by_id(session=session, department_id=department_id)
    if department:
        return department

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Department {department_id} not found"
    )


@router.put("/{department_id}/", response_model=Department)
async def update_department(department_id: int,
                            department_update: DepartmentUpdate,
                            session: AsyncSession = Depends(get_session)
                            ):

    updated_department = await crud.update_department(session=session, department_id=department_id,
                                                      department_update=department_update)

    if not updated_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department {department_id} not found"
        )

    if updated_department == department_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No changes were made"
        )

    return updated_department


@router.delete("/{department_id}/", response_model=dict)
async def delete_department(department_id: int,
                            session: AsyncSession = Depends(get_session),
                            current_user: dict = Depends(get_current_user)):

    success = await crud.delete_department(session=session, department_id=department_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department {department_id} not found"
        )

    return {"detail": f"Department {department_id} deleted successfully"}
