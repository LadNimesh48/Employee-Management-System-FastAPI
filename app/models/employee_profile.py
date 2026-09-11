from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base
from sqlalchemy.orm import relationship


class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"
    
    id          = Column(Integer, index=True, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
    phone       = Column(String)
    address     = Column(String)
    city        = Column(String)
    
    employee = relationship("Employee", back_populates="profile")