from typing import Optional

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str


class Department(DepartmentBase):
    id: Optional[int]

    class Config:
        from_attributes = True
