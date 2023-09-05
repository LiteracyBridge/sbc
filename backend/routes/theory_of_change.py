from typing import Dict, List, Optional
from datetime import datetime
from helpers.model_events import (
    delete_activity,
    delete_indicator,
    delete_theory_of_change,
)
from models import ProjectIndicators, TheoryOfChange, TheoryOfChangeIndicator
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from models import Monitoring, Risk, Activity
import models

router = APIRouter()


# ======== INDICATORS ========= #
@router.get("/{project_id}/indicators")
def get_project_indicators(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(ProjectIndicators)
        .filter(ProjectIndicators.project_id == project_id)
        .all()
    )


class IndicatorDto(BaseModel):
    data: List[Dict]


@router.post("/{item_id}/indicators")
def update_or_create_indicators(
    item_id: int, dto: IndicatorDto, db: Session = Depends(models.get_db)
):
    theory_of_change: TheoryOfChange | None = (
        db.query(TheoryOfChange).filter(TheoryOfChange.id == item_id).first()
    )
    if theory_of_change is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Add new Indikit indicators to project indicators
    # Save new Indikit indicators to theory of change indicators
    for item in dto.data:
        # Delete indicator
        if item.get("is_deleted", False):
            # Indicator is already in DB
            if item.get("id", None) is not None:
                delete_indicator(item["id"], db)

            # If not in DB, just skip it
            continue

        toc_indicator = TheoryOfChangeIndicator()
        is_new = True
        if item.get("id", None) is not None:
            result = (
                db.query(TheoryOfChangeIndicator)
                .filter(TheoryOfChangeIndicator.id == item["id"])
                .first()
            )
            if result is not None:
                toc_indicator = result
                is_new = False

        toc_indicator.theory_of_change_id = theory_of_change.id
        toc_indicator.indikit_id = item.get("indikit_id", None)
        toc_indicator.project_id = theory_of_change.project_id
        toc_indicator.name = item.get("name", None)

        if is_new:
            db.add(toc_indicator)

        db.commit()

        # Create monitoring item
        if is_new:
            record: Monitoring = Monitoring()
            record.toc_indicator_id = toc_indicator.id
            record.project_id = theory_of_change.project_id

            db.add(record)
            db.commit()

    return ApiResponse(data=get_toc_by_project_id(theory_of_change.project_id, db))


# =========== END: INDICATORS UPDATE =========== #


class TheoryOfChangeItemDto(BaseModel):
    id: Optional[int]
    type_id: int
    # from_id: Optional[str | int]
    to_id: Optional[str | int]
    links_to: Optional[List[int]]
    sem_id: Optional[int]
    name: str
    is_validated: Optional[bool] = False
    description: Optional[str]
    editing_user_id: Optional[int]
    new_indicators: Optional[List[Dict]] = None

    # Activity related fields
    intervention_id: Optional[int]
    driver_ids: Optional[List[int]]


class NewTheoryOfChangeDto(BaseModel):
    name: str
    project_id: int
    notes: Optional[str]


class RisksDto(BaseModel):
    id: Optional[int]
    name: Optional[str]
    mitigation: Optional[str]
    assumptions: Optional[str]
    risks: Optional[str]
    toc_from_id: Optional[int]
    toc_to_id: Optional[int]


def get_toc_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(TheoryOfChange)
        .filter(TheoryOfChange.project_id == projectId)
        .options(
            # subqueryload(models.TheoryOfChangeOld.graph)
            subqueryload(TheoryOfChange.indicators).subqueryload(
                TheoryOfChangeIndicator.indikit
            )
            # .options(
            #     subqueryload(models.TheoryOfChangeItem.sem),
            #     subqueryload(models.TheoryOfChangeItem.type),
            # )
        )
        # .options(joinedload(models.TheoryOfChange.graph))
        .all()
    )
    return record


@router.get("/{projectId}")
def get_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    return ApiResponse(data=get_toc_by_project_id(projectId, db))


@router.post("/{project_id}/item")
def update_or_create_item(
    project_id: int, dto: TheoryOfChangeItemDto, db: Session = Depends(models.get_db)
):
    toc = TheoryOfChange()

    if dto.id is not None:
        toc = db.query(TheoryOfChange).filter(TheoryOfChange.id == dto.id).first()

        if toc is None:
            raise HTTPException(status_code=404, detail="Item not found")
    else:
        # Name & type cannot be updated
        toc.type_id = dto.type_id
        toc.updated_at = datetime.now()

    toc.name = dto.name
    toc.links_to = dto.links_to
    toc.sem_id = dto.sem_id
    toc.description = dto.description
    toc.project_id = project_id
    toc.is_validated = dto.is_validated

    if dto.id is None:
        db.add(toc)

    db.commit()
    db.refresh(toc)

    # Create activity item
    if toc.type_id == 2:
        # TODO: update or create activity
        activity = Activity()
        is_new = True
        if dto.id is not None:
            resp = (
                db.query(Activity)
                .filter(Activity.theory_of_change_id == dto.id)
                .first()
            )
            activity = resp if resp is not None else Activity()

        activity.name = toc.name
        activity.notes = toc.description
        activity.prj_id = project_id
        activity.status_id = 1
        activity.editing_user_id = dto.editing_user_id
        activity.theory_of_change_id = toc.id
        activity.intervention_id = dto.intervention_id

        if is_new:
            db.add(activity)
        db.commit()


    # Create indicators
    if dto.new_indicators is not None:
        update_or_create_indicators(
            item_id=toc.id, dto=IndicatorDto(data=dto.new_indicators), db=db
        )

    return ApiResponse(data=get_toc_by_project_id(project_id, db))


@router.delete("/{project_id}/item/{item_id}")
def delete_toc_item(
    project_id: int,
    item_id: int,
    db: Session = Depends(models.get_db),
):
    record: TheoryOfChange | None = (
        db.query(TheoryOfChange).filter(TheoryOfChange.id == item_id).first()
    )

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Delete linked activity
    activity = (
        db.query(Activity).filter(Activity.theory_of_change_id == record.id).first()
    )
    if activity is not None:
        # Also deletes ToC item
        delete_activity(activity, db)
    else:
        # Handle related items deletion in event
        delete_theory_of_change(record.id, db)

    return get_by_project_id(project_id, db)


# ======== RISKS ========= #
@router.get("/{project_id}/risks")
def get_risks(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(Risk)
        .filter(Risk.project_id == project_id)
        .options(subqueryload(Risk.toc_from), subqueryload(Risk.toc_to))
        .all()
    )


@router.post("/{project_id}/risks")
def update_or_create_risk(
    project_id: int, dto: RisksDto, db: Session = Depends(models.get_db)
):
    risk: Risk = Risk()
    if dto.id is not None:
        temp = (
            db.query(Risk)
            .filter((Risk.id == dto.id) & (Risk.project_id == project_id))
            .first()
        )

        if temp is None:
            raise HTTPException(status_code=404, detail="Risk not found")
        risk = temp

    risk.name = dto.name
    risk.mitigation = dto.mitigation
    risk.assumptions = dto.assumptions
    risk.risks = dto.risks
    risk.toc_from_id = dto.toc_from_id
    risk.toc_to_id = dto.toc_to_id
    risk.project_id = project_id

    if dto.id is None:
        db.add(risk)

    db.commit()

    return get_risks(project_id, db)
