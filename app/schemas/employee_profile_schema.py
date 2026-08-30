

from pydantic import BaseModel

# from app.schemas.common_schema import EmployeeDepartmentResponse


class EmployeeProfileRequest(BaseModel):
   phone : str
   address : str
   city : str


class EmployeeProfileResponse(BaseModel):
    phone : str
    address : str
    city : str
