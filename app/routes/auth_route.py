from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest, LoginRespons, RefreshTokenRequest, CurrentUserResponse
from app.controllers.auth_controller import login_emp_controller, refresh_token_controller, login_google_user_controller
from fastapi.security import OAuth2PasswordRequestForm
from app.security.auth import get_current_user
from app.models.employee_model import Employee
from app.core.oauth import oauth

router = APIRouter()

@router.post("/login", response_model=LoginRespons)
# def login(payload: LoginRequest, db: Session = Depends(get_db)):
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = login_emp_controller(payload, db)
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return result

@router.post("/refresh-token")
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    refresh_token = refresh_token_controller(payload, db)
    print("Refresh Token:", refresh_token)
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    return refresh_token

@router.get("/current-user", response_model=CurrentUserResponse)
def get_current_user_info(current_user: Employee = Depends(get_current_user)):
    return current_user


@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):

    token = await oauth.google.authorize_access_token(request)
    # print(token)

    user = token["userinfo"]
    # print(user)

    google_access_token = login_google_user_controller(user, db)
    print(google_access_token)

    return google_access_token
