from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee_model import Employee
from app.models.refresh_token_model import RefreshToken
from app.security.hash import verify_password, hash_refresh_token
from app.security.jwt import create_access_token, create_refresh_token, decode_token, revork_all_session
from app.schemas.auth_schema import LoginRequest, RefreshTokenRequest
from app.core.config import REFRESH_TOKEN_EXPIRE_DAYS
from app.security.auth import login_employee


def login_emp_service(payload, db: Session):

    employee = db.query(Employee).filter(Employee.email == payload.username).first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(payload.password, employee.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return login_employee(employee, db)
    
    # token = create_access_token({"sub" : str(employee.id)})
    # refersh_token = create_refresh_token({"sub" : str(employee.id)})

    # hashRefreshToken = hash_refresh_token(refersh_token)

    # db_refresh_token = RefreshToken(
    #     token_hash = hashRefreshToken,
    #     employee_id = employee.id,
    #     expires_at = datetime.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
    #     # is_revoked = False
    #     # created_at = refersh_token["iat"]
    # )
    # db.add(db_refresh_token)
    # db.commit()

    # return {
    #     "access_token" : token,
    #     "refresh_token" : refersh_token,
    #     "token_type" : "bearer",
    # }


def refresh_token_service(payload: RefreshTokenRequest, db: Session):
    hashed_token = hash_refresh_token(payload.refresh_token)
    print("----Hashed ABC Refresh Token-----:", hashed_token)

    db_refresh_token = (db.query(RefreshToken).filter(RefreshToken.token_hash == hashed_token).first())
    print("----DB Refresh Token-----:", db_refresh_token)

    if not db_refresh_token:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Invalid refresh token")

    if db_refresh_token.is_revoked:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Refresh token already used")

    if db_refresh_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Refresh token expired")

    payload = decode_token(payload.refresh_token)
    print("----Decoded Payload-----:", payload)

    if not payload:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Invalid refresh token type")

    employee = db.query(Employee).filter(Employee.id == payload.get("sub")).first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Employee not found")

    revork_all_session(employee.id, db)

    token = create_access_token({"sub" : str(employee.id)})
    refersh_token = create_refresh_token({"sub" : str(employee.id)})

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


def login_google_user_service(user, db: Session):

    employee = db.query(Employee).filter(Employee.email == user["email"]).first()

    if employee is None:

        employee = Employee(
            name=user["name"],
            email=user["email"],
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)
    return login_employee(employee, db)
