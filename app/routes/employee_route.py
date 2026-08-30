from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.employee_schema import EmployeeRequest, EmployeeResponse, CustomeEmployeeResponse
from typing import Literal
from pydantic import EmailStr

from app.controllers.employee_controller import get_all_emp_controller, create_emp_controller, assign_employee_service

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
):
    return get_all_emp_controller(page, limit, sort_by, order, department, name, email, search, db)


@router.post("/", response_model=EmployeeResponse)
async def create_emp(payload: EmployeeRequest, db: Session = Depends(get_db)):
    return create_emp_controller(payload, db)

@router.post("/{employee_id}/skills/{skill_id}")
async def assign_skill(employee_id: int, skill_id: int, db: Session = Depends(get_db)):
    
    employee = assign_employee_service(employee_id, skill_id, db)
    
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee or Skill Not Found")
    
    return employee
    
