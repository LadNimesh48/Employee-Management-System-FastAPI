from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.skill_model import Skill
from app.schemas.skill_schema import SkillRquest, SkillResponse

import time


def get_all_skill_service(db: Session):

    start_time = time.perf_counter()
    getSkills = db.query(Skill).all()  # Lazy Loading
    # getSkills = (db.query(Skill).options(joinedload(Skill.employees)).all()) # Egle Loading->joinedload
    # getSkills = (db.query(Skill).options(selectinload(Skill.employees)).all()) # Egle Loading->selectinload

    if not getSkills:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Department not Found"
        )

    end_time = time.perf_counter()

    print(f"Total execution time: " f"{(end_time - start_time) * 1000:.2f} ms")

    return getSkills


def create_skill_service(payload: SkillRquest, db: Session):

    new_skill = Skill(
        name=payload.name,
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill
