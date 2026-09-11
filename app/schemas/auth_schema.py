from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    # email : EmailStr = Field(...)
    username : EmailStr = Field(...)
    password : str = Field(..., min_length=6)


class LoginRespons(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str


class RefreshTokenRequest(BaseModel):
    refresh_token : str = Field(..., min_length=6)

class CurrentUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    # department_id: int | None = None
    # role: str

class OTPRequest(BaseModel):
    email: EmailStr

class OTPverifyRequest(BaseModel):
    email: EmailStr
    otp: str