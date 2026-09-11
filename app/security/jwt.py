from datetime import  datetime,timedelta,timezone
from jose import jwt, JWTError
from app.core.config import SECRAT_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, status

from app.models.refresh_token_model import RefreshToken
from sqlalchemy.orm import Session


def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(to_encode, SECRAT_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(to_encode, SECRAT_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRAT_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # print("errors----:", e)
        # return JWTError
        print("JWT decode error:", e)

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def revork_all_session(employee_id: int, db: Session):
    db.query(RefreshToken).filter(RefreshToken.employee_id == employee_id).update({"is_revoked": True}, synchronize_session=False)
    db.commit()
