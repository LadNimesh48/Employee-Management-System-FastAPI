from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship
from app.models.associations import employee_skill


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    # department  = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    salary = Column(Integer)
    address = Column(String, nullable=True)

    department = relationship("Department", back_populates="employees")

    skills = relationship("Skill", secondary=employee_skill, back_populates="employees")
    
    profile = relationship("EmployeeProfile", back_populates="employee", cascade="all, delete", uselist=False)
