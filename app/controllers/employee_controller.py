from sqlalchemy.orm import Session
from app.services.employee_service import get_all_emp_service, create_emp_service, assign_employee_service


def get_all_emp_controller(page: int, limit: int,sort_by:str ,order: str, department: int, name: str, email: str, search: str, db: Session):
    return get_all_emp_service(page, limit, sort_by, order, department, name, email, search, db)

def create_emp_controller(payload, db: Session):
    return create_emp_service(payload, db)

def assign_employee_skills(employee_id: int, skill_id: int, db: Session):
    return assign_employee_service(employee_id, skill_id, db)