from typing import List, Optional
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from models import TheoryOfChangeIndicator, TheoryOfChange, TheoryOfChangeItem
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


@router.get("/{id}", response_model=ApiResponse)
def get_theory_of_change_details(id: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(models.TheoryOfChange)
        .filter(models.TheoryOfChange.id == id)
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

    return ApiResponse(data=[record])


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

    db.update(record)
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

    return get_theory_of_change_details(id, db)


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

    # db.update(record)
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

    return get_theory_of_change_details(id, db)


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

    return get_theory_of_change_details(id, db)


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

    db.delete()
    db.commit()

    return ApiResponse(data=[resp])


@router.post("/{id}/indicators", response_model=ApiResponse)
def update_indicators(id: int, dto: IndicatorDto, db: Session = Depends(models.get_db)):
    print(dto.removed)
    # Remove all indicators
    db.query(models.TheoryOfChangeIndicator).filter(
        TheoryOfChangeIndicator.theory_of_change_id == id,
        TheoryOfChangeIndicator.indicator_id.in_(dto.removed),
    ).delete()
    # for i in removed_indicators:
    #     db.delete(i)

    # Add all indicators
    new_indicators = []
    for i in dto.added:
        record = models.TheoryOfChangeIndicator()
        record.theory_of_change_id = id
        record.indicator_id = i

        new_indicators.append(record)

    db.add_all(new_indicators)
    db.commit()

    indicators = (
        db.query(models.TheoryOfChangeIndicator)
        .filter(TheoryOfChangeIndicator.theory_of_change_id == id)
        .options(subqueryload(TheoryOfChangeIndicator.indicator))
        .all()
    )

    return ApiResponse(data=indicators)


@router.get("/", response_model=ApiResponse)
def get_indicator(db: Session = Depends(models.get_db)):
    data = db.query(models.Indicator).all()

    return ApiResponse(data=data)
