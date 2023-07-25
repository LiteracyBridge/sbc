from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload, subqueryload
from model_events import delete_activity

import models
from models import Activity
from models import TheoryOfChange
from schema import ApiResponse

router = APIRouter()


# Types
class ActivityDto(BaseModel):
    id: Optional[int]
    name: str
    notes: Optional[str]
    url: Optional[str]
    prj_id: int
    parent_id: Optional[int]
    editing_user_id: Optional[int]
    toc_indicator_id: Optional[int]
    intervention_id: Optional[int]
    owner_id: Optional[int]
    status_id: Optional[int]
    driver_ids: Optional[List[int]]
    is_task: Optional[bool] = False
    end_date: Optional[str]
    start_date: Optional[str]


def get_toc_by_project_id(projectId: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(models.TheoryOfChangeOld)
        .filter(models.TheoryOfChangeOld.project_id == projectId)
        .first()
    )
    return record


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
def update_or_create(dto: ActivityDto, db: Session = Depends(models.get_db)):
    new_activity: Activity = Activity()

    if dto.id is not None:
        new_activity = db.query(Activity).filter(Activity.id == dto.id).first()

        if new_activity is None:
            return HTTPException(status_code=400, detail="Account cannot be created")

    new_activity.name = dto.name
    new_activity.url = dto.url
    new_activity.notes = dto.notes
    new_activity.prj_id = dto.prj_id
    new_activity.editing_user_id = dto.editing_user_id
    new_activity.theory_of_change_id = dto.toc_indicator_id
    new_activity.intervention_id = dto.intervention_id
    new_activity.owner_id = dto.owner_id
    new_activity.parent_id = dto.parent_id
    new_activity.status_id = dto.status_id
    new_activity.start_date = dto.start_date
    new_activity.end_date = dto.end_date

    if dto.driver_ids is None:
        new_activity.driver_ids = []
    else:
        new_activity.driver_ids = dto.driver_ids

    if dto.id is not None:
        db.commit()
        return get_project_activities(new_activity.prj_id, db)

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return get_project_activities(new_activity.prj_id, db)


@router.get("/{projectId}", response_model=ApiResponse)
def get_activities(projectId: int, db: Session = Depends(models.get_db)):
    return get_project_activities(project_id=projectId, db=db)


@router.delete("/{project_id}/{id}", response_model=ApiResponse)
def delete(project_id: int, id: int, db: Session = Depends(models.get_db)):
    activity = (
        db.query(Activity)
        .filter(Activity.id == id, Activity.prj_id == project_id)
        .first()
    )

    if activity is None:
        return HTTPException(status_code=400, detail="Account cannot be created")

    delete_activity(activity, db)

    # db.commit()

    return get_project_activities(project_id=project_id, db=db)
