from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import login_emp_service


def login_emp_controller(payload: LoginRequest, db: Session):
    return login_emp_service(payload, db)

