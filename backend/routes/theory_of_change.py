from typing import Optional
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session
from schema import ApiResponse
import models

router = APIRouter()


# Types
class IndicatorItem(BaseModel):
    id: str | int

class NewTheoryOfChangeDto(BaseModel):
    name: str
    project_id: int
    notes: Optional[str]


@router.post("/", response_model=ApiResponse)
def create(
    id: int, dto: NewTheoryOfChangeDto, db: Session = Depends(models.get_db)
):
    record = models.TheoryOfChange()
    record.name = dto.name
    record.project_id = dto.project_id
    record.notes = dto.notes

    if(dto.name is False):
        count = db.query(models.TheoryOfChange).filter(models.TheoryOfChange.project_id == dto.project_id).count()
        record.name = f"Theory of Change #${count + 1}"

    db.add(record)
    db.commit()
    db.refresh(record)

    return ApiResponse(data=record)


@router.post("/{id}/indicators", response_model=ApiResponse)
def add_indicator(
    id: int, indicator: IndicatorItem, db: Session = Depends(models.get_db)
):
    record = models.TheoryOfChangeIndicator()
    record.theory_of_change_id = id
    record.indicatory_id = indicator.id

    db.add(record)
    db.commit()
    db.refresh(record)

    return ApiResponse(data=record)


@router.get("/", response_model=ApiResponse)
def get_indicator(db: Session = Depends(models.get_db)):
    data = db.query(models.Indicator).all()

    return ApiResponse(data=data)
