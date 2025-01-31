from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str


class Department(DepartmentBase):
    id: int

    class Config:
        from_attributes = True
