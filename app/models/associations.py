from sqlalchemy import Table, Column, Integer, String, ForeignKey

from app.db.session import Base

employee_skill = Table(
    "employee_skills",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)
