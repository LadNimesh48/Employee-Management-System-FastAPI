from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.employee_model import Employee
from app.models.skill_model import Skill
from app.models.employee_profile import EmployeeProfile
from app.schemas.employee_schema import EmployeeRequest
from app.security.hash import hash_password
from sqlalchemy import func, or_
import time
from app.utils.email import send_welcome_email
from app.core.redis_server import redis_client
import json
from app.tasks.email_task import send_welcome_email_task


def get_all_emp_service(page: int, limit: int, sort_by:str, order: str, department: int, name: str, email: str, search: str, db: Session):

    # getEmployeeData = db.query(Employee).all()
    start_time = time.perf_counter()

    skip = (page-1)*limit

    # query = db.query(Employee).options(joinedload(Employee.profile))
    query = db.query(Employee).options(joinedload(Employee.profile), joinedload(Employee.skills), joinedload(Employee.department))

    sort_by = getattr(Employee, sort_by)

    if order == "desc":
        query = query.order_by(sort_by.desc())
    else:
        query = query.order_by(sort_by.asc())

    # Department wise filter
    # if department:
    #     query = query.filter( func.lower(Employee.department) == func.lower(department))

    if department:
        query = query.filter(Employee.department_id.ilike(department.strip()))

    if name:
        query = query.filter(Employee.name.ilike(f"%{name.strip()}%"))

    # if email:
    #     query = query.filter(Employee.email.ilike(email.strip()))

    if email:
        query = query.filter(Employee.email.ilike(f"%{email.strip()}%"))

    if search:
        search = search.strip()

        query = query.filter(
            or_(
                Employee.name.ilike(f"%{search}%"),
                Employee.department.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%")
            )
        )

    # print(query)
    getEmployeeData = (query.offset(skip).limit(limit).all())

    result = []

    for employee in getEmployeeData:

        result.append(
            {
                "id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "address": employee.address,
                "department": (
                    [{"id": employee.department.id, "name": employee.department.name}]
                    if employee.department
                    else []
                ),
                "skills": [
                    {"id": skill.id, "name": skill.name} for skill in employee.skills
                ],
                "phone": (employee.profile.phone if employee.profile else None),
                "city": (employee.profile.city if employee.profile else None),
            }
        )

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employees data Not Found")

    end_time = time.perf_counter()

    print(
        f"Total execution time: "
        f"{(end_time - start_time) * 1000:.2f} ms"
    )

    return result

def create_emp_service(payload: EmployeeRequest, image_path, db: Session):

    start_time = time.perf_counter()
    new_employee = Employee(
        # **payload.model_dump()
        name=payload.name,
        email=payload.email,
        # department=payload.department,
        salary=payload.salary,
        # address=payload.address,
        password=hash_password(payload.password),
        role_id = payload.role_id,
        profile_image = image_path
    )
    
    profile = EmployeeProfile(
        phone = payload.profile.phone,
        address=payload.profile.address,
        city = payload.profile.city,
    )
    
    new_employee.profile = profile

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    # save Into Redis Using employee ID Key
    
    redis_client.set(
        f"employee:{new_employee.id}",
        json.dumps({
            "id":new_employee.id,
            "name": new_employee.name,
            "email": new_employee.email,
            "profile_image":new_employee.profile_image
        })
    )
    
    # Send welcome email in background
    # background_tasks.add_task(send_welcome_email,new_employee.email,new_employee.name)
    send_welcome_email_task.delay(new_employee.email, new_employee.name)
    
    end_time = time.perf_counter()
    print(f"Total execution time: " f"{(end_time - start_time) * 1000:.2f} ms")

    return new_employee


def assign_employee_service(employee_id: int, skill_id: int, db: Session):
    
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Not Found")
    
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    
    if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill Not Found")
    
    if skill not in employee.skills:
        employee.skills.append(skill)
    
    db.commit()
    db.refresh(employee)
    
    return {"msg" : "Skill Assigned Successfully"}


def get_emp_ByID_service(employee_id : int,  db: Session):

    start_time = time.perf_counter()

    cache_key = f"employee:{employee_id}"
    cached_employee = redis_client.get(cache_key)

    if cached_employee:

        end_time = time.perf_counter()
        print(f"Total execution time: " f"{(end_time - start_time) * 1000:.2f} ms")

        print('From Redis Server')
        return json.loads(cached_employee)

    print('From DB Server')
    getEmployeeByID = (db.query(Employee).filter(Employee.id == employee_id).first())

    if getEmployeeByID is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee Data Not Found of ID : {employee_id}")

    # Convert SQLAlchemy object to dictionary
    employee_data = {
        column.name: getattr(getEmployeeByID, column.name)
        for column in Employee.__table__.columns
    }

    redis_client.set(cache_key,json.dumps(employee_data, default=str),ex=3600)
    print(f"Employee {employee_id} saved in Redis")

    end_time = time.perf_counter()
    print(f"Total execution time: " f"{(end_time - start_time) * 1000:.2f} ms")

    return getEmployeeByID


def delete_emp_ByID_service(employee_id: int, db: Session):

    getEmployeeByID = db.query(Employee).filter(Employee.id == employee_id).first()

    if getEmployeeByID is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EMployee Data Not Found")

    db.delete(getEmployeeByID)
    db.commit()

    redis_client.delete(f"employee:{employee_id}")

    return {"msg": "Employee Deleted Successfully"}
