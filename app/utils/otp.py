import random
from app.core.redis_server import redis_client
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.employee_model import Employee
from fastapi import HTTPException, status


def generate_otp():
    return str(random.randint(100000, 999999))


def create_otp(email: EmailStr, db:Session):

    getEmployee = db.query(Employee).filter(Employee.email == email).first()

    if not getEmployee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Details Not Found")

    otp = generate_otp()

    redis_key = f"otp:{email}"
    redis_client.setex(redis_key, 300, otp)

    return getEmployee,otp


def verify_otp(email: EmailStr, otp: str, db: Session):

    redis_key = f"otp:{email}"
    print(redis_key)

    stored_otp = redis_client.get(redis_key)
    print("stored_otp")
    print(stored_otp)

    if stored_otp is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Expired")

    if stored_otp != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP Invalid")

    redis_client.delete(redis_key)

    employee = db.query(Employee).filter(Employee.email == email).first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Details Not Found")

    return employee
