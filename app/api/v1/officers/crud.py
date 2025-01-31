from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import Officer
from app.api.v1.officers.schemas import OfficerCreate, OfficerUpdate


async def get_officers(session: AsyncSession) -> List[Officer]:
    result = await session.execute(select(Officer))
    officers = result.scalars().all()
    return list(officers)


async def get_officer_by_id(session: AsyncSession, officer_id: int) -> Optional[dict]:
    officer = await session.get(Officer, officer_id)
    if officer:
        return {"id": officer.id,
                "first_name": officer.first_name,
                "last_name": officer.last_name}
    return None


async def create_officer(session: AsyncSession, officer: OfficerCreate) -> Officer:
    new_officer = Officer(**officer.model_dump())
    session.add(new_officer)
    await session.commit()
    await session.refresh(new_officer)
    return new_officer


async def update_officer(session: AsyncSession,
                         officer_id: int,
                         officer_update: OfficerUpdate
                         ) -> Optional[Officer]:
    result = await session.execute(select(Officer).filter(Officer.id == officer_id))
    officer = result.scalar_one_or_none()

    if officer:
        officer.name = officer_update.first_name
        officer.last_name = officer_update.last_name
        officer.email = officer_update.email
        session.add(officer)
        await session.commit()
        await session.refresh(officer)
        return officer
    return None


async def delete_officer(session: AsyncSession,
                         officer_id: int
                         ) -> bool:
    result = await session.execute(select(Officer).filter(Officer.id == officer_id))
    officer = result.scalar_one_or_none()

    if officer:
        await session.delete(officer)
        await session.commit()
        return True
    return False
