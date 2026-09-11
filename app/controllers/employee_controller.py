from sqlalchemy.orm import Session
from app.services.employee_service import get_all_emp_service, create_emp_service, assign_employee_service, get_emp_ByID_service, delete_emp_ByID_service
from app.utils.file_upload import upload_file


def get_all_emp_controller(page: int, limit: int,sort_by:str ,order: str, department: int, name: str, email: str, search: str, db: Session):
    return get_all_emp_service(page, limit, sort_by, order, department, name, email, search, db)

def create_emp_controller(background_tasks, payload, profile_image, db: Session):
    image_path = upload_file(profile_image)
    return create_emp_service(background_tasks, payload, image_path, db)

def assign_employee_skills(employee_id: int, skill_id: int, db: Session):
    return assign_employee_service(employee_id, skill_id, db)


def get_emp_ByID_controller(employee_id : int,  db: Session):
    return get_emp_ByID_service(employee_id, db)

def delete_emp_ByID_controller(employee_id : int,  db: Session):
    return delete_emp_ByID_service(employee_id, db)