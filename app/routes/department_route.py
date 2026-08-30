from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.department_schema import DepartmentRequest, DepartmentResponse
from app.controllers.department_controller import get_all_department_controller, create_department_controller


router = APIRouter()

@router.get("/", response_model=list[DepartmentResponse])
def get_department(db: Session = Depends(get_db)):
    return get_all_department_controller(db)

@router.post("/", response_model=DepartmentResponse)
def create_department(payload:DepartmentRequest,  db: Session = Depends(get_db)):
    return create_department_controller(payload, db)

