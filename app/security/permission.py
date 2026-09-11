from fastapi import Depends, HTTPException, status
from app.models.employee_model import Employee
from app.security.auth import get_current_user


def required_role(*roles):
    
    def role_check(current_user: Employee = Depends(get_current_user)):
        print("current_user........", current_user.__dict__)
        if current_user.role_id not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you don't have permission to access this URL")
        
        return current_user

    return role_check