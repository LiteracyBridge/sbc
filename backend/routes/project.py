from typing import List, Optional, Dict

from sqlalchemy import text
from models import ProjectIndicators
from helpers import ToCItemDto, create_toc_item

import models
from fastapi import APIRouter, Depends, HTTPException
from models import ProjectData
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session

router = APIRouter()


# Types
class UpdateProjectDto(BaseModel):
    # name: str
    evaluation_strategy: Optional[str]
    feedback_strategy: Optional[str]


class ProjectObjectiveDto(BaseModel):
    # name: str
    # module: str
    editing_user_id: int

    updated: List[Dict[str, str]] = []
    added: Optional[List[str]] = []
    removed: Optional[List[int]] = []


@router.get("/{id}", response_model=ApiResponse)
def find_project(id: int, db: Session = Depends(models.get_db)):
    record = db.query(models.Project).filter(models.Project.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return ApiResponse(data=[record])


@router.put("/{id}", response_model=ApiResponse)
def update_strategy(
    id: int, dto: UpdateProjectDto, db: Session = Depends(models.get_db)
):
    record = db.query(models.Project).filter(models.Project.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # record.name = dto.name
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


# Project objectives route
@router.get("/{project_id}/data", response_model=ApiResponse)
def get_project_data(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
    )


@router.post("/{project_id}/objectives", response_model=ApiResponse)
def update_objectives(
    project_id: int, dto: ProjectObjectiveDto, db: Session = Depends(models.get_db)
):
    """Manage project objectives"""

    # Remove deleted objectives
    if len(dto.removed) > 0:
        db.query(ProjectData).filter(ProjectData.id.in_(dto.removed)).delete()

    # Update existing objectives
    if len(dto.updated) > 0:
        for item in dto.updated:
            [value] = item.values()
            [key] = item.keys()

            record = db.query(ProjectData).filter(ProjectData.id == int(key)).first()

            if record is None:
                continue

            # FIXME: Update corresponding theory of change item
            record.data = value
            db.commit()

    # Create new objectives
    if len(dto.added) > 0:
        for item in dto.added:
            record: ProjectData = ProjectData()
            record.q_id = 10
            record.data = item
            record.module = "objectives"
            record.name = "specific_objectives"
            record.prj_id = project_id
            record.editing_user_id = dto.editing_user_id

            db.add(record)
            db.commit()
            db.refresh(record)

            # Create theory of change objective item
            toc = create_toc_item(
                ToCItemDto(
                    project_id=project_id,
                    name=item,
                    reference=record,
                    type="objective",
                ),
                db=db,
            )

            record.theory_of_change_id = toc.id
            db.commit()

    return ApiResponse(
        data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
    )


@router.post("/{project_id}/audience", response_model=ApiResponse)
def update_audience(
    project_id: int, dto: ProjectObjectiveDto, db: Session = Depends(models.get_db)
):
    """Manage project audiences"""

    # Remove deleted audiences
    if len(dto.removed) > 0:
        db.query(ProjectData).filter(ProjectData.id.in_(dto.removed)).delete()

    # Update existing audiences
    if len(dto.updated) > 0:
        for item in dto.updated:
            [value] = item.values()
            [key] = item.keys()

            record = db.query(ProjectData).filter(ProjectData.id == int(key)).first()

            if record is None:
                continue

            record.data = value
            db.commit()

    # Create new objectives
    if len(dto.added) > 0:
        for item in dto.added:
            record: ProjectData = ProjectData()
            record.q_id = 3
            record.data = item
            record.module = "audiences"
            record.name = "secondary_audiences"
            record.prj_id = project_id
            record.editing_user_id = dto.editing_user_id

            db.add(record)
            db.commit()

    return ApiResponse(
        data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
    )
