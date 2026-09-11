from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.department_model import Department
from app.schemas.department_schema import DepartmentRequest
from sqlalchemy import func, or_
import time


def get_all_department_service(db: Session):
    
    start_time = time.perf_counter()
    # getDepartmentData = db.query(Department).all() #Lazy Loading
    # getDepartmentData = (db.query(Department).options(joinedload(Department.employees)).all()) # Egle Loading->joinedload
    getDepartmentData = (db.query(Department).options(selectinload(Department.employees)).all()) # Egle Loading->selectinload
    
    if not getDepartmentData:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not Found")
    
    end_time = time.perf_counter()
    
    print(
        f"Total execution time: "
        f"{(end_time - start_time) * 1000:.2f} ms"
    )
    
    return getDepartmentData

def create_department_service(payload:DepartmentRequest, db: Session):
    
    new_dept = Department(
            name=payload.name,
        )
    
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)

    return new_dept
    
    