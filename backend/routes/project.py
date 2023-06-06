from typing import List, Optional

import models
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from models import Activity, Project, TheoryOfChangeItem, User
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, joinedload, subqueryload

router = APIRouter()


# Types
class UpdateProjectDto(BaseModel):
    name: str
    evaluation_strategy: Optional[str]
    feedback_strategy: Optional[str]


@router.get("/{userEmail}", response_model=ApiResponse)
def update_strategy(email: str, db: Session = Depends(models.get_db)):
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    projects = (
        db.query(Project).filter(Project.organisation_id == user.organisation_id).all()
    )

    return ApiResponse(data=[projects])


@router.put("/{id}", response_model=ApiResponse)
def update_strategy(dto: UpdateProjectDto, db: Session = Depends(models.get_db)):
    record = db.query(models.Project).filter(models.Project.id == dto.id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Project not found")

    record.name = dto.name
    record.evaluation_strategy = dto.evaluation_strategy
    record.feedback_strategy = dto.feedback_strategy

    db.commit()
    db.refresh(record)

    return ApiResponse(data=[record])
