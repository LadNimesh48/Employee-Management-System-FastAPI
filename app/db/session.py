from sqlalchemy.orm import sessionmaker, Session , declarative_base
from app.db.database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False,  bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
