from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest, LoginRespons
from app.controllers.auth_controller import login_emp_controller

router = APIRouter()

@router.post("/login", response_model=LoginRespons)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_emp_controller(payload, db)