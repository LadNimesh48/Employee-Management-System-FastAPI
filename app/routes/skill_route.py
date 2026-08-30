from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.skill_schema import SkillRquest, SkillResponse
from app.controllers.skill_controller import get_all_skill_controller, create_skill_controller


router = APIRouter()

@router.get("/", response_model=list[SkillResponse])
def get_skill(db: Session = Depends(get_db)):
    return get_all_skill_controller(db)

@router.post("/", response_model=SkillResponse)
def create_skill(payload:SkillRquest,  db: Session = Depends(get_db)):
    return create_skill_controller(payload, db)

