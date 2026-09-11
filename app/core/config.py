from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRAT_KEY = os.getenv("SECRAT_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_SECRET_ID = os.getenv("GOOGLE_SECRET_ID")

class RoleConfig(BaseSettings):
    USER_ROLE_ID: int = 1
    ADMIN_ROLE_ID: int = 2
    MANAGER_ROLE_ID: int = 3
    

role_config = RoleConfig()