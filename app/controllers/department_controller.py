from sqlalchemy.orm import Session
from app.services.department_service import get_all_department_service,create_department_service


def get_all_department_controller(db: Session):
    return get_all_department_service(db)

def create_department_controller(payload, db: Session):
    return create_department_service(payload, db)