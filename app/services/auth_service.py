from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_model import Employee
from app.security.hash import verify_password
from app.security.jwt import create_access_token
from app.schemas.auth_schema import LoginRequest





def login_emp_service(payload: LoginRequest, db: Session):
    
    employee = db.query(Employee).filter(Employee.email == payload.email).first()
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not verify_password(payload.password, employee.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_access_token({"sub" : employee.id})
    
    return {
        "access_token" : token,
        "token_type" : "bearer"
    }