from typing import Optional, List

import models
from fastapi import APIRouter, Depends
from models import (
    Communication,
    CommunicationAudience,
    CommunicationIndicator,
    CommunicationObjective,
)
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, subqueryload
from datetime import datetime

router = APIRouter()


class CommunicationDto(BaseModel):
    title: str
    message_objectives: Optional[str]
    delivery_platforms: Optional[str]
    format: Optional[str]
    contents: str
    key_points: Optional[str]
    target_audiences: List[int]
    indicators: List[int]
    project_objectives: List[int]


@router.get("/{project_id}", response_model=ApiResponse)
def find_all(project_id: int, db: Session = Depends(models.get_db)):
    results = (
        db.query(Communication)
        .filter(Communication.project_id == project_id)
        .options(
            subqueryload(Communication.target_audiences),
            subqueryload(Communication.indicators),
            subqueryload(Communication.project_objectives),
        )
        .all()
    )

    return ApiResponse(data=results)


@router.delete("/{project_id}/{id}", response_model=ApiResponse)
def delete(project_id: int, id: int, db: Session = Depends(models.get_db)):
    db.query(Communication).filter(
        Communication.id == id and Communication.project_id == project_id
    ).delete()
    db.commit()

    return find_all(project_id, db)


@router.post("/{project_id}", response_model=ApiResponse)
def create(
    project_id: int, dto: CommunicationDto, db: Session = Depends(models.get_db)
):
    new_comm: CommunicationDto = Communication()
    new_comm.project_id = project_id
    new_comm.title = dto.title
    new_comm.message_objectives = dto.message_objectives
    new_comm.format = dto.format
    new_comm.key_points = dto.key_points
    new_comm.contents = dto.contents
    new_comm.delivery_platforms = dto.delivery_platforms
    new_comm.updated_at = datetime.now().isoformat()

    db.add(new_comm)
    db.commit()
    db.refresh(new_comm)

    # Create target audiences
    audiences: List[CommunicationIndicator] = []
    for id in dto.target_audiences:
        audience = CommunicationAudience()
        audience.communication_id = new_comm.id
        audience.audience_id = id

        audiences.append(audience)

    indicators: List[CommunicationIndicator] = []
    for id in dto.indicators:
        indicator = CommunicationIndicator()
        indicator.communication_id = new_comm.id
        indicator.indicator_id = id

        indicators.append(indicator)

    objectives: List[CommunicationObjective] = []
    for id in dto.project_objectives:
        objective = CommunicationObjective()
        objective.communication_id = new_comm.id
        objective.objective_id = id

        objectives.append(objective)

    db.add_all(objectives)
    db.add_all(audiences)
    db.add_all(indicators)
    db.commit()

    return find_all(project_id, db)
