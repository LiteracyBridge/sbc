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


def get_monitoring_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(Monitoring).filter(Monitoring.project_id == projectId)
        .options(
            subqueryload(Monitoring.toc_item_indicator)
            .subqueryload(TheoryOfChangeIndicator.indicator)
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
