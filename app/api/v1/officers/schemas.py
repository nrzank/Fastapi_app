from pydantic import BaseModel, EmailStr
from typing import Optional


class OfficerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int

    class Config:
        from_attributes = True


class OfficerCreate(OfficerBase):
    pass


class Officer(OfficerBase):
    id: int

    class Config:
        from_attributes = True


class OfficerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None

    class Config:
        from_attributes = True
