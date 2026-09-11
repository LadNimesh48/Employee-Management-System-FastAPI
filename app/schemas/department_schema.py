from sqlalchemy import Column
from app.db.session import Base
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.schemas.common_schema import EmployeeDepartmentResponse


class DepartmentRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=30)


class DepartmentResponse(BaseModel):
    id: int
    name: str
    employees: list[EmployeeDepartmentResponse] = []
