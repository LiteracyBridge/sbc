from typing import Dict, List, Optional
from db_models.project import ProjectIndicators, TheoryOfChange, TheoryOfChangeIndicator
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from models import (
    Monitoring,
    Risk,
    TheoryOfChangeOld,
    # TheoryOfChangeItem,
)
import models

router = APIRouter()


# Types
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
    type_id: str | int
    from_id: Optional[str | int]
    to_id: Optional[str | int]
    sem_id: str | int
    name: str
    is_validated: Optional[bool] = False
    description: Optional[str]


class NewTheoryOfChangeDto(BaseModel):
    name: str
    project_id: int
    notes: Optional[str]


class RisksDto(BaseModel):
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


# def get_toc_by_id(id: int, db: Session = Depends(models.get_db)):
#     record = (
#         db.query(models.TheoryOfChangeOld)
#         .filter(models.TheoryOfChangeOld.id == id)
#         .options(
#             subqueryload(models.TheoryOfChangeOld.risks),
#             subqueryload(models.TheoryOfChangeOld.graph).subqueryload(
#                 TheoryOfChangeIndicator.indicators
#             )
#             # .subqueryload(TheoryOfChangeIndicator.indicator),
#             # .options(
#             #     subqueryload(models.TheoryOfChangeItem.sem),
#             #     subqueryload(models.TheoryOfChangeItem.type),
#             # )
#         )
#         # .options(joinedload(models.TheoryOfChange.graph))
#         .first()
#     )

#     return ApiResponse(data=[record])


@router.post("/", response_model=ApiResponse)
def create(dto: NewTheoryOfChangeDto, db: Session = Depends(models.get_db)):
    record = models.TheoryOfChangeOld()
    record.name = dto.name
    record.project_id = dto.project_id
    record.notes = dto.notes

    if dto.name is False:
        count = (
            db.query(models.TheoryOfChangeOld)
            .filter(models.TheoryOfChangeOld.project_id == dto.project_id)
            .count()
        )
        record.name = f"Theory of Change #${count + 1}"

    db.add(record)
    db.commit()
    db.refresh(record)

    return ApiResponse(data=record)


@router.get("/{projectId}", response_model=ApiResponse)
def get_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    return ApiResponse(data=get_toc_by_project_id(projectId, db))


@router.post("/{project_id}/item", response_model=ApiResponse)
def create_item(
    project_id: int, dto: TheoryOfChangeItemDto, db: Session = Depends(models.get_db)
):
    record = TheoryOfChange()
    record.name = dto.name
    record.type_id = dto.type_id
    record.from_id = dto.from_id
    record.to_id = dto.to_id
    record.sem_id = dto.sem_id
    record.description = dto.description
    record.project_id = project_id

    db.add(record)
    db.commit()

    # Create activity item if toc item is an activity

    # if dto.to_id is not None:
    #     # Query for the to_id and link it to the from_id
    #     to_record = (
    #         db.query(models.TheoryOfChangeItem)
    #         .filter(models.TheoryOfChangeItem.id == dto.to_id)
    #         .first()
    #     )
    #     to_record.from_id = record.id

    #     db.add(to_record)
    #     db.commit()

    # db.refresh(record)

    return ApiResponse(data=get_toc_by_project_id(project_id, db))


@router.put("/{project_id}/item/{itemId}", response_model=ApiResponse)
def update_item(
    project_id: int,
    itemId: int,
    dto: TheoryOfChangeItemDto,
    db: Session = Depends(models.get_db),
):
    record = (
        db.query(TheoryOfChange)
        .filter(TheoryOfChange.id == itemId)
        .first()
    )

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    record.name = dto.name
    record.type_id = dto.type_id
    record.from_id = dto.from_id
    record.to_id = dto.to_id
    record.sem_id = dto.sem_id
    record.description = dto.description
    record.is_validated = dto.is_validated

    db.commit()

    return ApiResponse(data=get_by_project_id(project_id, db))


@router.delete("/{id}/item/{itemId}", response_model=ApiResponse)
def delete_item(
    id: int,
    itemId: int,
    db: Session = Depends(models.get_db),
):
    record = db.query(TheoryOfChange).filter(TheoryOfChange.id == itemId).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Reset all the from_id
    db.query(TheoryOfChange).filter(TheoryOfChange.from_id == record.id).update(
        {"from_id": None}
    )

    # Reset all the to_id
    db.query(TheoryOfChange).filter(TheoryOfChange.to_id == record.id).update(
        {"to_id": None}
    )

    # Delete the record
    db.delete(record)
    db.commit()

    return ApiResponse(data=get_by_project_id(id, db))


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
    # TODO: Add to project indicators first

    # Remove deleted indicators
    if dto.removed is not None:
        db.query(TheoryOfChangeIndicator).filter(
            TheoryOfChangeIndicator.theory_of_change_id == item_id,
            TheoryOfChangeIndicator.indicator_id.in_(dto.removed),
        ).delete()

    theory_of_change = (
        db.query(TheoryOfChange).filter(TheoryOfChange.id == item_id).first()
    )
    if theory_of_change is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Add new indikit indicators to project indicators
    if dto.added is not None:
        print(dto.added)
        new_toc_indicators = list(
            map(
                lambda x: x["id"],
                list(filter(lambda x: x["id"] is not None, dto.added)),
            )
        )
        print(new_toc_indicators)

        existing_project_indicators = (
            db.query(ProjectIndicators)
            .filter(ProjectIndicators.project_id == theory_of_change.project_id)
            .with_entities(ProjectIndicators.id)
            .all()
        )
        print(existing_project_indicators)

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
            record = TheoryOfChangeIndicator()
            record.indicator_id = i
            record.theory_of_change_id = item_id
            record.project_id = theory_of_change.project_id
            record.indicator_id = i

            db.add(record)
            db.commit()
            db.refresh(record)
            monitoring_indicators.append(record.id)

        # Create monitoring items
        monitoring_items = []
        for i in monitoring_indicators:
            record = Monitoring()
            record.toc_item_indicator_id = i
            record.project_id = theory_of_change.project_id

            monitoring_items.append(record)

        db.add_all(monitoring_items)
        db.commit()
    # # Add all indicators
    # new_indicators = []
    # for i in dto.added:
    #     record = TheoryOfChangeIndicator()
    #     record.toc_item_id = item_id
    #     record.indicator_id = i

    #     new_indicators.append(record)

    # db.add_all(new_indicators)
    # db.commit()

    # Fetch theory of change
    # toc_item = (
    #     db.query(models.TheoryOfChangeItem)
    #     .filter(models.TheoryOfChangeItem.id == item_id)
    #     .first()
    # )
    # toc = get_toc_by_id(toc_item.theory_of_change_id, db)

    # # Create monitoring item
    # toc_indicators = (
    #     db.query(models.TheoryOfChangeIndicator)
    #     .filter(
    #         TheoryOfChangeIndicator.toc_item_id == item_id,
    #         TheoryOfChangeIndicator.indicator_id.in_(dto.added),
    #     )
    #     .all()
    # )

    # monitoring_indicators = []
    # for i in toc_indicators:
    #     record = Monitoring()
    #     record.toc_item_indicator_id = i.id
    #     record.project_id = toc.data[0].project_id

    #     monitoring_indicators.append(record)

    # db.add_all(monitoring_indicators)
    # db.commit()

    return ApiResponse(data=get_toc_by_project_id(theory_of_change.project_id, db))


@router.get("/", response_model=ApiResponse)
def get_indicator(db: Session = Depends(models.get_db)):
    data = db.query(models.Indicator).all()

    return ApiResponse(data=data)


@router.post("/{tocId}/risks", response_model=ApiResponse)
def risks(tocId: int, dto: RisksDto, db: Session = Depends(models.get_db)):
    toc = db.query(TheoryOfChange).filter(TheoryOfChange.id == tocId).first()
    risk = Risk()

    risk.name = dto.name
    risk.mitigation = dto.mitigation
    risk.assumptions = dto.assumptions
    risk.risks = dto.risks
    risk.toc_from_id = dto.toc_from_id
    risk.toc_to_id = dto.toc_to_id
    risk.theory_of_change_id = tocId

    db.add(risk)
    db.commit()

    return ApiResponse(data=get_by_project_id(toc.project_id, db))
