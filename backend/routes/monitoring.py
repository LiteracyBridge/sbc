from functools import reduce
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session, joinedload, subqueryload
from schema import ApiResponse
from models import TheoryOfChangeIndicator, TheoryOfChange
from models import Monitoring
import models

router = APIRouter()


class UpdateMonitoringDto(BaseModel):
    target: Optional[str]
    baseline: Optional[str]
    type: Optional[str]
    # TODO: calculate progress on the frontend
    # progress: Optional[int]
    data_collection_method: Optional[str]
    reporting_period: Optional[str]


class RecordProgressDto(BaseModel):
    value: Optional[int]
    period: Optional[str]
    progress: Optional[str]


def get_monitoring_by_project_id(
    projectId: int, db: Session = Depends(models.get_db)
) -> List[Monitoring]:
    record = (
        db.query(Monitoring)
        .filter(Monitoring.project_id == projectId)
        .options(
            subqueryload(Monitoring.toc_indicator).options(
                subqueryload(TheoryOfChangeIndicator.indikit),
                subqueryload(TheoryOfChangeIndicator.theory_of_change),
                # subqueryload(TheoryOfChangeIndicator.toc_item),
            ),
        )
        .order_by(Monitoring.id.desc())
        .all()
    )
    return record


@router.get("/{projectId}")
def get_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    return ApiResponse(data=get_monitoring_by_project_id(projectId, db))


@router.put("/{id}")
def update_item(
    id: int,
    dto: UpdateMonitoringDto,
    db: Session = Depends(models.get_db),
):
    record: Monitoring | None = db.query(Monitoring).filter(Monitoring.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    record.target = dto.target
    record.baseline = dto.baseline
    record.data_collection_method = dto.data_collection_method
    record.reporting_period = dto.reporting_period
    record.type = dto.type

    db.commit()

    return ApiResponse(data=get_monitoring_by_project_id(record.project_id, db))


@router.post("/{id}/evaluation")
def record_progress(
    id: int,
    dto: RecordProgressDto,
    db: Session = Depends(models.get_db),
):
    # TODO: rewrite progress tracking
    record: Monitoring | None = db.query(Monitoring).filter(Monitoring.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    evaluation = record.evaluation
    if evaluation is None:
        evaluation = []

    evaluation.append({"period": dto.period, "value": dto.value})
    record.evaluation = evaluation
    record.progress = dto.progress

    db.commit()

    return ApiResponse(data=get_monitoring_by_project_id(record.project_id, db))
