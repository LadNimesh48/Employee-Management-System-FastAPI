from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.security.jwt import create_access_token, create_refresh_token, decode_token
from app.models.employee_model import Employee
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS
from app.models.refresh_token_model import RefreshToken
from app.security.hash import hash_refresh_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is invalid or expired")

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Token is not an access token")

    employee = db.query(Employee).filter(Employee.id == int(payload.get("sub"))).first()

    if employee is None:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Employee not found")

    return employee


def login_employee(employee, db: Session):

    payload = {"sub": str(employee.id)}
    
    
    token = create_access_token(payload)
    refersh_token = create_refresh_token(payload)
    
    hashRefreshToken = hash_refresh_token(refersh_token)
    # print("----Hashed Refresh Token-----:", hashRefreshToken)

    db_refresh_token = RefreshToken(
        token_hash = hashRefreshToken,
        employee_id = employee.id,
        expires_at = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
        # is_revoked = False
        # created_at = refersh_token["iat"]
    )
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token" : token,
        "refresh_token" : refersh_token,
        "token_type" : "bearer",
    }