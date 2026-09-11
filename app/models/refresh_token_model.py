from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from app.db.session import Base
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta, timezone

class RefreshToken(Base):

    __tablename__ = "refresh_tokens"
    
    id         = Column(Integer, index=True, primary_key=-True, autoincrement=True)
    token_hash  = Column(String, unique=True, nullable=False)
    employee_id  = Column(Integer, ForeignKey("employees.id"), nullable=False)
    # expires_at  = Column(DateTime, nullable=False)
    expires_at = Column(DateTime(timezone=True),nullable=False)
    is_revoked  = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.now(timezone.utc))
    
    employee = relationship("Employee", back_populates="refresh_tokens")