from typing import List, Optional

from sqlalchemy import text

import models
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from models import Activity, Project, TheoryOfChangeItem, User
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, joinedload, subqueryload
from fastapi.encoders import jsonable_encoder

router = APIRouter()


# Types
class UpdateProjectDto(BaseModel):
    name: str
    evaluation_strategy: Optional[str]
    feedback_strategy: Optional[str]


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


@router.get("/drivers/{project_id}")
def get_project_drivers(project_id: int, db: Session = Depends(models.get_db)):
    statement = text(
        """
    SELECT ld.id AS lu_id,
        ld.parent_id,
        ld.category_id,
        ld.name,
        ld.intervention_ids,
        dp.id AS dip_id,
        dp.prj_id
    FROM lu_drivers ld
    INNER JOIN drivers_in_prj dp ON
        ld.id = dp.lu_driver_id
         AND dp.prj_id = :project_id
         AND ld.intervention_ids IS NOT NULL;
        """
    )

    drivers = db.execute(statement, {"project_id": project_id}).all()
    return ApiResponse(data=[row._asdict() for row in drivers])
