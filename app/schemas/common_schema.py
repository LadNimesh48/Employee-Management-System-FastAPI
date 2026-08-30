from pydantic import BaseModel, EmailStr


class DepartmentEmployeeResponse(BaseModel):
    name: str


class EmployeeDepartmentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class EmployeeSkillsResponse(BaseModel):
    id: int
    name: str

class CustomeDepartmentResponse(BaseModel):
    id: int
    name: str

class CustomeSkillResponse(BaseModel):
    id: int
    name: str
