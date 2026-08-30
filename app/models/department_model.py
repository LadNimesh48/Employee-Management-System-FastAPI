from sqlalchemy import Column, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = "departments"
    
    id      = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name    = Column(String, nullable=False, unique=True)
    
    employees   = relationship("Employee", back_populates="department", cascade="all, delete")