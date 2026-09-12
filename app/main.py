from fastapi import FastAPI
from app.routes import app_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.exception import exception_middleware
from app.middleware.rate_limit import rate_limit_middleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Employee Management System")

app.middleware("http")(exception_middleware)
app.middleware("http")(rate_limit_middleware)

app.add_middleware(SessionMiddleware, secret_key="my-google-login-secret-key")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(app_router)


@app.get("/")
def home():
    return {"message": "Employee Management System API"}