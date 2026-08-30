from sqlalchemy import Column, Integer, String
from app.db.session import Base
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from app.schemas.common_schema import DepartmentEmployeeResponse, EmployeeSkillsResponse, CustomeDepartmentResponse, CustomeSkillResponse
from app.schemas.employee_profile_schema import EmployeeProfileRequest, EmployeeProfileResponse


class EmployeeRequest(BaseModel):

    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    # department  : str       = Field(..., min_length=2)
    salary: float | int = Field(..., gt=0)
    password : str = Field(..., min_length=6)
    profile : EmployeeProfileRequest


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    # address : str
    address: Optional[str] = None
    # department_id : int | None = None
    department: Optional[DepartmentEmployeeResponse] | None = None
    skills: list[EmployeeSkillsResponse] = []
    profile: EmployeeProfileResponse | None = None
    
    model_config = ConfigDict( from_attribute=True )
    
    
class CustomeEmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: Optional[str] = None

    # department: Optional[str] = None
    # skills: List[str] = []
    
    department: List[CustomeDepartmentResponse] = []
    skills: List[CustomeSkillResponse] = []


    phone: Optional[str] = None
    city: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
