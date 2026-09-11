from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.associations import employee_skill
from app.db.session import Base

class Skill(Base):
    __tablename__ = "skills"
    
    id      = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name    = Column(String, unique=True)

    employees = relationship("Employee", secondary=employee_skill  , back_populates="skills")