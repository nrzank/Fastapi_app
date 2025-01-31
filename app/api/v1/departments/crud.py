from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import Department
from app.api.v1.departments.schemas import DepartmentCreate, DepartmentUpdate


async def get_departments(session: AsyncSession) -> List[Department]:
    result = await session.execute(select(Department))
    departments = result.scalars().all()
    return list(departments)


async def get_department_by_id(session: AsyncSession,
                               department_id: int
                               ) -> Optional[Department]:

    return await session.get(Department, department_id)


async def create_department(session: AsyncSession,
                            department: DepartmentCreate
                            ) -> Department:

    new_department = Department(name=department.name)
    session.add(new_department)
    await session.commit()
    await session.refresh(new_department)
    return new_department


async def update_department(session: AsyncSession,
                            department_id: int,
                            department_update: DepartmentUpdate
                            ) -> Optional[Department]:

    result = await session.execute(select(Department).filter(Department.id == department_id))
    department = result.scalar_one_or_none()

    if department:
        department.name = department_update.name
        session.add(department)
        await session.commit()
        await session.refresh(department)
        return department
    return None


async def delete_department(session: AsyncSession,
                            department_id: int
                            ) -> bool:

    result = await session.execute(select(Department).filter(Department.id == department_id))
    department = result.scalar_one_or_none()

    if department:
        await session.delete(department)
        await session.commit()
        return True
    return False