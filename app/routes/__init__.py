from fastapi import APIRouter
from app.routes.employee_route import router as employee_router
from app.routes.department_route import router as department_router
from app.routes.skill_route import router as skill_router
from app.routes.auth_route import router as auth_route

import app.models
# from app.db.session import Base
# from app.db.database import engine

# Base.metadata.create_all(engine)


app_router = APIRouter()

app_router.include_router(employee_router, prefix="/employee", tags=["employee"])
app_router.include_router(department_router, prefix="/department", tags=["department"])
app_router.include_router(skill_router, prefix="/skill", tags=["skill"])
app_router.include_router(auth_route, prefix="/auth", tags=["Auth"])