from typing import Dict, List, Optional
from model_events import theory_of_change_deleted
from models import ProjectIndicators, TheoryOfChange, TheoryOfChangeIndicator
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from models import Monitoring, Risk, Activity
import models

router = APIRouter()


class IndicatorDto(BaseModel):
    # TODO: remove these
    removed: List[int]
    # removed_indi_kit: List[int]
    # added: List[int]

    # added_indi_kit: Optional[List[Dict]]
    # removed_indi_kit: Optional[List[int]]

    added: Optional[List[Dict]]
    removed_custom: Optional[List[int]]


class TheoryOfChangeItemDto(BaseModel):
    type_id: int
    # from_id: Optional[str | int]
    to_id: Optional[str | int]
    links_to: Optional[List[int]]
    sem_id: Optional[int]
    name: str
    is_validated: Optional[bool] = False
    description: Optional[str]
    editing_user_id: Optional[int]


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
            subqueryload(TheoryOfChange.indicators)
            .subqueryload(TheoryOfChangeIndicator.indicator)
            .options(subqueryload(ProjectIndicators.indi_kit)),
            # .options(
            #     subqueryload(models.TheoryOfChangeItem.sem),
            #     subqueryload(models.TheoryOfChangeItem.type),
            # )
        )
        # .options(joinedload(models.TheoryOfChange.graph))
        .all()
    )
    return record


@router.get("/{projectId}", response_model=ApiResponse)
def get_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    return ApiResponse(data=get_toc_by_project_id(projectId, db))


@router.post("/{project_id}/item", response_model=ApiResponse)
def create_item(
    project_id: int, dto: TheoryOfChangeItemDto, db: Session = Depends(models.get_db)
):
    toc: TheoryOfChange = TheoryOfChange()
    toc.name = dto.name
    toc.type_id = dto.type_id
    # toc.from_id = dto.from_id
    # toc.to_id = dto.to_id
    toc.links_to = dto.links_to
    toc.sem_id = dto.sem_id
    toc.description = dto.description
    toc.project_id = project_id

    # todo: use helper method
    db.add(toc)
    db.commit()
    db.refresh(toc)

    # Create activity item
    if toc.type_id == 2:
        new_activity: Activity = Activity()
        new_activity.name = toc.name
        new_activity.notes = toc.description
        new_activity.prj_id = project_id
        new_activity.status_id = 1
        new_activity.editing_user_id = dto.editing_user_id
        new_activity.theory_of_change_id = toc.id

        db.add(new_activity)
        db.commit()

    return ApiResponse(data=get_toc_by_project_id(project_id, db))


@router.put("/{project_id}/item/{itemId}", response_model=ApiResponse)
def update_item(
    project_id: int,
    itemId: int,
    dto: TheoryOfChangeItemDto,
    db: Session = Depends(models.get_db),
):
    record = db.query(TheoryOfChange).filter(TheoryOfChange.id == itemId).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    record.name = dto.name
    # record.type_id = dto.type_id
    # record.from_id = dto.from_id
    record.links_to = dto.links_to
    record.sem_id = dto.sem_id
    record.description = dto.description
    record.is_validated = dto.is_validated

    db.commit()

    return get_by_project_id(project_id, db)


@router.delete("/{project_id}/item/{itemId}", response_model=ApiResponse)
def delete_item(
    project_id: int,
    itemId: int,
    db: Session = Depends(models.get_db),
):
    record = db.query(TheoryOfChange).filter(TheoryOfChange.id == itemId).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Reset all the from_id
    # db.query(TheoryOfChange).filter(TheoryOfChange.from_id == record.id).update(
    #     {"from_id": None}
    # )

    # db.query(TheoryOfChangeIndicator).filter(
    #     TheoryOfChangeIndicator.theory_of_change_id == record.id
    # ).delete()
    # db.query(Risk).filter(Risk.toc_from_id == record.id).delete()

    # Reset all the to_id
    # db.query(TheoryOfChange).filter(TheoryOfChange.to_id == record.id).update(
    #     {"to_id": None}
    # )


    # Handle related items deletion in event
    theory_of_change_deleted(record, db)

    # Delete the record
    record.delete()

    # db.delete()
    # db.delete(record)
    db.commit()
    # db.

    return get_by_project_id(project_id, db)


# ======== INDICATORS ========= #
@router.get("/{project_id}/indicators", response_model=ApiResponse)
def get_project_indicators(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(ProjectIndicators)
        .filter(ProjectIndicators.project_id == project_id)
        .all()
    )


@router.post("/{item_id}/indicators", response_model=ApiResponse)
def update_indicators(
    item_id: int, dto: IndicatorDto, db: Session = Depends(models.get_db)
):
    print(dto)
    # Remove deleted indicators
    if dto.removed is not None:
        records = (
            db.query(TheoryOfChangeIndicator)
            .filter(
                TheoryOfChangeIndicator.theory_of_change_id == item_id,
                TheoryOfChangeIndicator.id.in_(dto.removed),
            )
            .delete()
        )
        db.commit()

    theory_of_change = (
        db.query(TheoryOfChange).filter(TheoryOfChange.id == item_id).first()
    )
    if theory_of_change is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Add new Indikit indicators to project indicators
    if dto.added is not None:
        new_toc_indicators = list(
            map(
                lambda x: x["id"],
                list(filter(lambda x: x["id"] is not None, dto.added)),
            )
        )

        existing_project_indicators = (
            db.query(ProjectIndicators)
            .filter(ProjectIndicators.project_id == theory_of_change.project_id)
            .with_entities(ProjectIndicators.id)
            .all()
        )

        # 1. Add to project indicators for new items
        new_project_indicators = list(
            filter(lambda x: x["id"] is None or x["indi_kit_id"] is not None, dto.added)
        )

        for item in new_project_indicators:
            if item["indi_kit_id"] is not None:
                # Check if already exists
                if item["indi_kit_id"] in existing_project_indicators:
                    continue

            record = ProjectIndicators()
            record.name = item["name"]
            record.indi_kit_id = item["indi_kit_id"]
            record.project_id = theory_of_change.project_id

            db.add(record)
            db.commit()
            db.refresh(record)
            new_toc_indicators.append(record.id)

        # Update theory of change indicators
        monitoring_indicators = []
        for i in new_toc_indicators:
            record: TheoryOfChangeIndicator = TheoryOfChangeIndicator()
            record.indicator_id = i
            record.theory_of_change_id = item_id
            record.project_id = theory_of_change.project_id
            record.indicator_id = i

            db.add(record)
            db.commit()
            db.refresh(record)
            monitoring_indicators.append(record.id)

        # Create monitoring items
        for i in monitoring_indicators:
            record: Monitoring = Monitoring()
            record.toc_indicator_id = i
            record.project_id = theory_of_change.project_id

            db.add(record)
            db.commit()

    return ApiResponse(data=get_toc_by_project_id(theory_of_change.project_id, db))


# @router.get("/", response_model=ApiResponse)
# def get_indicator(db: Session = Depends(models.get_db)):
#     data = db.query(models.Indicator).all()

#     return ApiResponse(data=data)


# ======== RISKS ========= #
@router.get("/{project_id}/risks", response_model=ApiResponse)
def get_risks(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(Risk)
        .filter(Risk.project_id == project_id)
        .options(subqueryload(Risk.toc_from), subqueryload(Risk.toc_to))
        .all()
    )


@router.post("/{project_id}/risks", response_model=ApiResponse)
def update_or_create_risk(
    project_id: int, dto: RisksDto, db: Session = Depends(models.get_db)
):
    risk: Risk = Risk()
    if dto.id is not None:
        risk = (
            db.query(Risk)
            .filter(Risk.id == dto.id and Risk.project_id == project_id)
            .first()
        )

        if risk is None:
            raise HTTPException(status_code=404, detail="Risk not found")

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
