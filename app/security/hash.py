from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_hash_password(plainpassword: str, hashpassword):
    return pwd_context.verify(plainpassword,hashpassword)