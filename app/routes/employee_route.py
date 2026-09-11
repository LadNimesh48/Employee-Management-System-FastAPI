from fastapi import APIRouter, Depends, File, Form, Query, HTTPException, status, UploadFile, BackgroundTasks
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.employee_schema import EmployeeRequest, EmployeeResponse, CustomeEmployeeResponse, EmployeeByIDResponse
from typing import Literal
from pydantic import EmailStr
from app.security.auth import get_current_user
from app.models.employee_model import Employee
from app.security.permission import required_role
from app.core.config import role_config

from app.controllers.employee_controller import get_all_emp_controller, create_emp_controller, assign_employee_service, get_emp_ByID_controller, delete_emp_ByID_controller
from app.schemas.employee_profile_schema import EmployeeProfileRequest

router = APIRouter()


@router.get("/", response_model=list[CustomeEmployeeResponse])
async def get_employees(
    page    : int = Query(1, ge=1),
    limit   : int = Query(5, ge=1, le=50),
    sort_by : Literal["id", "name", "salary"]   = "id",
    order   : Literal["asc", "desc"]            = "asc",
    department : int | None = None,
    name    : str | None = None,
    # email   : EmailStr | None = None,
    email   : str | None = None,
    search  : str | None = None,
    db      : Session = Depends(get_db),
    current_user: Employee = Depends(required_role(role_config.MANAGER_ROLE_ID, role_config.ADMIN_ROLE_ID, role_config.USER_ROLE_ID))
):
    return get_all_emp_controller(page, limit, sort_by, order, department, name, email, search, db)


@router.post("/", response_model=EmployeeResponse)
# async def create_emp(payload: EmployeeRequest, db: Session = Depends(get_db), current_user: Employee = Depends(required_role(role_config.MANAGER_ROLE_ID, role_config.ADMIN_ROLE_ID))):
async def create_emp(
    background_tasks: BackgroundTasks,
    name: str = Form(),
    email: EmailStr = Form(),
    salary: float | int = Form(),
    password: str = Form(),
    role_id: int = Form(),
    profile_image: UploadFile = File(...),
    phone: str = Form(),
    address: str = Form(),
    city: str = Form(),
    db: Session = Depends(get_db),
    current_user: Employee = Depends(required_role(role_config.MANAGER_ROLE_ID, role_config.ADMIN_ROLE_ID)),
):

    payload = EmployeeRequest(
        name=name,
        email=email,
        salary=salary,
        password=password,
        role_id=role_id,
        profile=EmployeeProfileRequest(
            phone   = phone,
            address = address,
            city= city,
            ),
    )

    return create_emp_controller(background_tasks,payload, profile_image, db)


@router.post("/{employee_id}/skills/{skill_id}")
async def assign_skill(employee_id: int, skill_id: int, db: Session = Depends(get_db), current_user: Employee = Depends(required_role(role_config.MANAGER_ROLE_ID, role_config.ADMIN_ROLE_ID))):
    
    employee = assign_employee_service(employee_id, skill_id, db)
    
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee or Skill Not Found")
    
    return employee


@router.get("/{employee_id}", response_model=EmployeeByIDResponse)
def get_emp_ByID(employee_id : int,  db: Session = Depends(get_db)):
    return get_emp_ByID_controller(employee_id, db)


@router.delete("/{employee_id}/delete")
def delete_emp_ByID(employee_id : int,  db: Session = Depends(get_db)):
    return delete_emp_ByID_controller(employee_id, db)