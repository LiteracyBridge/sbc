from functools import reduce
from typing import List, Optional
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from db_models.project import TheoryOfChangeIndicator, TheoryOfChange
from models import Monitoring
import models

router = APIRouter()


class UpdateMonitoringDto(BaseModel):
    target: Optional[int]
    baseline: Optional[int]
    # progress: Optional[int]
    data_collection_method: Optional[str]
    data_collection_frequency: Optional[str]
    evaluation_period: Optional[str]


class RecordProgressDto(BaseModel):
    value: Optional[int]
    period: Optional[str]


def get_monitoring_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(Monitoring)
        .filter(Monitoring.project_id == projectId)
        .options(
            subqueryload(Monitoring.toc_item_indicator).options(
                subqueryload(TheoryOfChangeIndicator.indicator),
                # subqueryload(TheoryOfChangeIndicator.toc_item),
            )
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
    record.data_collection_method = dto.data_collection_method
    record.data_collection_frequency = dto.data_collection_frequency
    record.evaluation_period = dto.evaluation_period

    db.commit()

    return ApiResponse(data=get_monitoring_by_project_id(record.project_id, db))


@router.post("/{id}/evaluation", response_model=ApiResponse)
def record_progress(
    id: int,
    dto: RecordProgressDto,
    db: Session = Depends(models.get_db),
):
    record = db.query(Monitoring).filter(Monitoring.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    evaluation = record.evaluation
    if evaluation is None:
        evaluation = {}

    evaluation[dto.period] = dto.value
    record.evaluation = evaluation
    record.progress = (sum(evaluation.values()) / record.target) * 100

    db.commit()

    return ApiResponse(data=get_monitoring_by_project_id(record.project_id, db))
