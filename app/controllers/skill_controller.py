from sqlalchemy.orm import Session
from app.services.skill_service import get_all_skill_service, create_skill_service


def get_all_skill_controller(db: Session):
    return get_all_skill_service(db)

def create_skill_controller(payload, db: Session):
    return create_skill_service(payload, db)