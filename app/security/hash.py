from passlib.context import CryptContext
import hashlib


pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def hash_refresh_token(refresh_token: str):
    return hashlib.sha256(refresh_token.encode()).hexdigest()