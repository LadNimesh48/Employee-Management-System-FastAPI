from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.employee_model import Employee
from app.models.skill_model import Skill
from app.models.employee_profile import EmployeeProfile
from app.schemas.employee_schema import EmployeeRequest
from app.security.hash import hash_password
from sqlalchemy import func, or_
import time



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

def create_emp_service(payload: EmployeeRequest, db: Session):

    new_employee = Employee(
        # **payload.model_dump()
        name=payload.name,
        email=payload.email,
        # department=payload.department,
        salary=payload.salary,
        # address=payload.address,
        password=hash_password(payload.password)
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
