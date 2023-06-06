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


class UpdateMonitoringDto(BaseModel):
    target: Optional[int]
    baseline: Optional[int]
    # progress: Optional[int]
    data_collection_method: Optional[str]
    data_collection_frequency: Optional[str]
    evaluation_period: Optional[str]


def get_monitoring_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(Monitoring)
        .filter(Monitoring.project_id == projectId)
        .options(
            subqueryload(Monitoring.toc_item_indicator).subqueryload(
                TheoryOfChangeIndicator.indicator
            )
            #     .subqueryload(TheoryOfChangeItem.indicators)
            #     .subqueryload(TheoryOfChangeIndicator.indicator),
        )
        # .options(joinedload(models.TheoryOfChange.graph))
        .all()
    )
    return record


def get_monitoring_by_id(id: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(Monitoring)
        .filter(Monitoring.id == id)
        .options(
            subqueryload(Monitoring.toc_item_indicator).subqueryload(
                TheoryOfChangeIndicator.indicator
            )
            #     .subqueryload(TheoryOfChangeItem.indicators)
            #     .subqueryload(TheoryOfChangeIndicator.indicator),
        )
        # .options(joinedload(models.TheoryOfChange.graph))
        .all()
    )
    return record


@router.get("/{projectId}", response_model=ApiResponse)
def get_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    return ApiResponse(data=get_monitoring_by_project_id(projectId, db))


@router.put("/{id}", response_model=ApiResponse)
def update_item(
    id: int,
    dto: UpdateMonitoringDto,
    db: Session = Depends(models.get_db),
):
    record = db.query(Monitoring).filter(Monitoring.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    record.target = dto.target
    record.baseline = dto.baseline
    # record.progress = dto.progress
    record.data_collection_method = dto.data_collection_method
    record.data_collection_frequency = dto.data_collection_frequency
    record.evaluation_period = dto.evaluation_period

    db.commit()

    return ApiResponse(data=get_monitoring_by_project_id(record.project_id, db))
