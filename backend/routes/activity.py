from typing import List, Optional

import models
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from models import Activity
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, joinedload, subqueryload

router = APIRouter()


# Types
class ActivityDto(BaseModel):
    id: Optional[int]
    name: str
    notes: Optional[str]
    url: Optional[str]
    prj_id: int
    editing_user_id: Optional[int]
    toc_indicator_id: Optional[int]
    intervention_id: Optional[int]
    owner_id: Optional[int]
    status_id: Optional[int]
    driver_ids: Optional[List[int]]


def get_project_activities(project_id: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(Activity)
        .filter(Activity.prj_id == project_id)
        .all()
        # .options(
        #     subqueryload(models.TheoryOfChange.risks),
        #     subqueryload(models.TheoryOfChange.graph)
        #     .subqueryload(TheoryOfChangeItem.indicators)
        #     .subqueryload(TheoryOfChangeIndicator.indicator),
        #     # .options(
        #     #     subqueryload(models.TheoryOfChangeItem.sem),
        #     #     subqueryload(models.TheoryOfChangeItem.type),
        #     # )
        # )
        # # .options(joinedload(models.TheoryOfChange.graph))
        # .first()
        # TODO: load related models
    )

    return ApiResponse(data=record)


@router.post("/", response_model=ApiResponse)
def create(dto: ActivityDto, db: Session = Depends(models.get_db)):
    record: Activity = Activity()
    record.name = dto.name
    record.url = dto.url
    record.notes = dto.notes
    record.prj_id = dto.prj_id
    record.editing_user_id = dto.editing_user_id
    record.toc_indicator_id = dto.toc_indicator_id
    record.intervention_id = dto.intervention_id
    record.owner_id = dto.owner_id
    record.status_id = dto.status_id
    record.driver_ids = dto.driver_ids

    db.add(record)
    db.commit()
    db.refresh(record)

    # return ApiResponse(data=[record])
    return get_project_activities(record.prj_id, db)


@router.get("/{projectId}", response_model=ApiResponse)
def get_activities(projectId: int, db: Session = Depends(models.get_db)):
    return get_project_activities(project_id=projectId, db=db)
