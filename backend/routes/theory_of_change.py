from typing import List, Optional
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from models import (
    Monitoring,
    Risk,
    TheoryOfChangeIndicator,
    TheoryOfChange,
    TheoryOfChangeItem,
)
import models

router = APIRouter()


# Types
class IndicatorDto(BaseModel):
    removed: List[int]
    added: List[int]


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
        db.query(models.TheoryOfChange)
        .filter(models.TheoryOfChange.project_id == projectId)
        .options(
            subqueryload(models.TheoryOfChange.graph)
            .subqueryload(TheoryOfChangeItem.indicators)
            .subqueryload(TheoryOfChangeIndicator.indicator),
            # .options(
            #     subqueryload(models.TheoryOfChangeItem.sem),
            #     subqueryload(models.TheoryOfChangeItem.type),
            # )
        )
        # .options(joinedload(models.TheoryOfChange.graph))
        .first()
    )
    return record


def get_toc_by_id(id: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(models.TheoryOfChange)
        .filter(models.TheoryOfChange.id == id)
        .options(
            subqueryload(models.TheoryOfChange.risks),
            subqueryload(models.TheoryOfChange.graph)
            .subqueryload(TheoryOfChangeItem.indicators)
            .subqueryload(TheoryOfChangeIndicator.indicator),
            # .options(
            #     subqueryload(models.TheoryOfChangeItem.sem),
            #     subqueryload(models.TheoryOfChangeItem.type),
            # )
        )
        # .options(joinedload(models.TheoryOfChange.graph))
        .first()
    )

    return ApiResponse(data=[record])


@router.post("/", response_model=ApiResponse)
def create(dto: NewTheoryOfChangeDto, db: Session = Depends(models.get_db)):
    record = models.TheoryOfChange()
    record.name = dto.name
    record.project_id = dto.project_id
    record.notes = dto.notes

    if dto.name is False:
        count = (
            db.query(models.TheoryOfChange)
            .filter(models.TheoryOfChange.project_id == dto.project_id)
            .count()
        )
        record.name = f"Theory of Change #${count + 1}"

    db.add(record)
    db.commit()
    db.refresh(record)

    return ApiResponse(data=record)


@router.get("/{projectId}", response_model=ApiResponse)
def get_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    return ApiResponse(data=[get_toc_by_project_id(projectId, db)])


@router.post("/{id}/item", response_model=ApiResponse)
def create_item(
    id: int, dto: TheoryOfChangeItemDto, db: Session = Depends(models.get_db)
):
    record = models.TheoryOfChangeItem()
    record.name = dto.name
    record.type_id = dto.type_id
    record.from_id = dto.from_id
    record.to_id = dto.to_id
    record.sem_id = dto.sem_id
    record.description = dto.description
    record.theory_of_change_id = id

    db.add(record)
    db.commit()

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

    return get_toc_by_id(id, db)


@router.put("/{id}/item/{itemId}", response_model=ApiResponse)
def update_item(
    id: int,
    itemId: int,
    dto: TheoryOfChangeItemDto,
    db: Session = Depends(models.get_db),
):
    record = (
        db.query(models.TheoryOfChangeItem)
        .filter(models.TheoryOfChangeItem.id == itemId)
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

    return get_toc_by_id(id, db)


@router.delete("/{id}/item/{itemId}", response_model=ApiResponse)
def delete_item(
    id: int,
    itemId: int,
    db: Session = Depends(models.get_db),
):
    record = (
        db.query(models.TheoryOfChangeItem)
        .filter(models.TheoryOfChangeItem.id == itemId)
        .first()
    )

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Reset all the from_id
    db.query(models.TheoryOfChangeItem).filter(
        models.TheoryOfChangeItem.from_id == record.id
    ).update({"from_id": None})

    # Reset all the to_id
    db.query(models.TheoryOfChangeItem).filter(
        models.TheoryOfChangeItem.to_id == record.id
    ).update({"to_id": None})

    # Delete the record
    db.delete(record)
    db.commit()

    return get_toc_by_id(id, db)


@router.post("/{id}/item/{item_id}", response_model=ApiResponse)
def add_item(id: int, item_id: int, db: Session = Depends(models.get_db)):
    resp = (
        db.query(models.TheoryOfChangeItem)
        .filter(
            models.TheoryOfChangeItem.id == item_id,
            models.TheoryOfChangeItem.theory_of_change_id == id,
        )
        .first()
    )

    db.delete(resp)
    db.commit()

    return ApiResponse(data=[resp])


@router.post("/{itemId}/indicators", response_model=ApiResponse)
def update_indicators(
    itemId: int, dto: IndicatorDto, db: Session = Depends(models.get_db)
):
    db.query(models.TheoryOfChangeIndicator).filter(
        TheoryOfChangeIndicator.toc_item_id == itemId,
        TheoryOfChangeIndicator.indicator_id.in_(dto.removed),
    ).delete()

    # Add all indicators
    new_indicators = []
    for i in dto.added:
        record = models.TheoryOfChangeIndicator()
        record.toc_item_id = itemId
        record.indicator_id = i

        new_indicators.append(record)

    db.add_all(new_indicators)
    db.commit()

    # Fetch theory of change
    toc_item = (
        db.query(models.TheoryOfChangeItem)
        .filter(models.TheoryOfChangeItem.id == itemId)
        .first()
    )
    toc = get_toc_by_id(toc_item.theory_of_change_id, db)

    # Create monitoring item
    toc_indicators = (
        db.query(models.TheoryOfChangeIndicator)
        .filter(
            TheoryOfChangeIndicator.toc_item_id == itemId,
            TheoryOfChangeIndicator.indicator_id.in_(dto.added),
        )
        .all()
    )

    monitoring_items = []
    for i in toc_indicators:
        record = Monitoring()
        record.toc_item_indicator_id = i.id
        record.project_id = toc.data[0].project_id

        monitoring_items.append(record)

    db.add_all(monitoring_items)
    db.commit()

    return get_toc_by_id(toc_item.theory_of_change_id, db)


@router.get("/", response_model=ApiResponse)
def get_indicator(db: Session = Depends(models.get_db)):
    data = db.query(models.Indicator).all()

    return ApiResponse(data=data)


@router.post("/{tocId}/risks", response_model=ApiResponse)
def risks(tocId: int, dto: RisksDto, db: Session = Depends(models.get_db)):
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

    return get_toc_by_id(tocId, db)
