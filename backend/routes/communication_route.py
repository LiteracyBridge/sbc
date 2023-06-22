from typing import Optional, List

import models
from fastapi import APIRouter, Depends
from models import (
    Communication,
    CommunicationAudience,
    CommunicationDriver,
    CommunicationIndicator,
    CommunicationObjective,
)
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, subqueryload
from datetime import datetime

router = APIRouter()


class CommunicationDto(BaseModel):
    id: Optional[int]
    title: str
    message_objectives: Optional[str]
    delivery_platforms: Optional[str]
    format: Optional[str]
    contents: str
    key_points: Optional[str]
    target_audiences: List[int]
    indicators: List[int]
    project_objectives: List[int]
    drivers: List[int]


@router.get("/{project_id}", response_model=ApiResponse)
def find_all(project_id: int, db: Session = Depends(models.get_db)):
    results = (
        db.query(Communication)
        .filter(Communication.project_id == project_id)
        .options(
            subqueryload(Communication.target_audiences),
            subqueryload(Communication.indicators),
            subqueryload(Communication.project_objectives),
            subqueryload(Communication.drivers),
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
def update_or_create(
    project_id: int, dto: CommunicationDto, db: Session = Depends(models.get_db)
):
    updating = dto.id is not None
    comm: CommunicationDto = Communication()

    if updating:
        comm = (
            db.query(Communication)
            .filter(Communication.id == dto.id and Communication.project_id == dto.id)
            .options(
                subqueryload(Communication.target_audiences),
                subqueryload(Communication.indicators),
                subqueryload(Communication.project_objectives),
                subqueryload(Communication.drivers),
            )
            .first()
        )

        if comm is None:
            return ApiResponse(success=False, message="Communication not found")

    comm.project_id = project_id
    comm.title = dto.title
    comm.message_objectives = dto.message_objectives
    comm.format = dto.format
    comm.key_points = dto.key_points
    comm.contents = dto.contents
    comm.delivery_platforms = dto.delivery_platforms
    comm.updated_at = datetime.now().isoformat()

    if not updating:
        db.add(comm)

    db.commit()
    db.refresh(comm)

    # Delete audiences that are not in the new list
    for audience in comm.target_audiences:
        if not any(id == audience.audience_id for id in dto.target_audiences):
            db.delete(audience)

    # Create or update target audiences
    audiences: List[CommunicationIndicator] = []
    for id in dto.target_audiences:
        if not any(d.id == id for d in comm.target_audiences):
            audience = CommunicationAudience()
            audience.communication_id = comm.id
            audience.audience_id = id

            audiences.append(audience)

    # Delete audiences that are not in the new list
    for ind in comm.indicators:
        if not any(id == ind.indicator_id for id in dto.indicators):
            db.delete(ind)

    # Update or create indicators
    indicators: List[CommunicationIndicator] = []
    for id in dto.indicators:
        if not any(d.id == id for d in comm.indicators):
            indicator = CommunicationIndicator()
            indicator.communication_id = comm.id
            indicator.indicator_id = id

            indicators.append(indicator)

    # Delete objectives that are not in the new list
    for obj in comm.project_objectives:
        if not any(id == obj.objective_id for id in dto.project_objectives):
            db.delete(obj)

    # Update or create objectives
    objectives: List[CommunicationObjective] = []
    for id in dto.project_objectives:
        if not any(d.id == id for d in comm.project_objectives):
            objective = CommunicationObjective()
            objective.communication_id = comm.id
            objective.objective_id = id

            objectives.append(objective)

    # Delete drivers that are not in the new list
    for obj in comm.drivers:
        if not any(id == obj.driver_id for id in dto.drivers):
            db.delete(obj)

    # Update or create drivers
    drivers: List[CommunicationDriver] = []
    for id in dto.drivers:
        if not any(d.id == id for d in comm.drivers):
            driver = CommunicationDriver()
            driver.communication_id = comm.id
            driver.driver_id = id

            drivers.append(driver)

    db.add_all(objectives)
    db.add_all(audiences)
    db.add_all(drivers)
    db.commit()

    return find_all(project_id, db)
