from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest, RefreshTokenRequest
from app.services.auth_service import login_emp_service, refresh_token_service, login_google_user_service


def login_emp_controller(payload, db: Session):
    return login_emp_service(payload, db)

def refresh_token_controller(payload:RefreshTokenRequest , db: Session):
    return refresh_token_service(payload, db)

def login_google_user_controller(user, db: Session):
    return login_google_user_service(user, db)