from pydantic import BaseModel
from app.schemas.employee_schema import EmployeeResponse

class SkillRquest(BaseModel):
    name : str

class SkillResponse(BaseModel):
    id: int
    name: str
    employees: list[EmployeeResponse] = []