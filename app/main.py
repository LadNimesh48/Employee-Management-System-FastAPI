from fastapi import FastAPI
from app.routes import app_router

app = FastAPI(title="Employee Management System")


app.include_router(app_router)

@app.get("/")
def home():
    return {"message": "Employee Management System API"}