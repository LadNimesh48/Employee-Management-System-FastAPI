from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    email : EmailStr = Field(...)
    password : str = Field(..., min_length=6)


class LoginRespons(BaseModel):
    access_token : str
    token_type : str
    