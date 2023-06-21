from typing import List, Optional
from helpers import ToCItemDto, create_toc_item

import models
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from models import Activity
from models import TheoryOfChange
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, joinedload, subqueryload

router = APIRouter()


# Types
class ActivityDto(BaseModel):
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
def create(dto: ActivityDto, db: Session = Depends(models.get_db)):
    new_activity: Activity = Activity()
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

    if dto.driver_ids is None:
        new_activity.driver_ids = []
    else:
        new_activity.driver_ids = dto.driver_ids

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    if not dto.is_task:
        create_toc_item(
            dto=ToCItemDto(
                project_id=dto.prj_id,
                type="activity",
                name=dto.name,
                reference=new_activity,
            ),
            db=db,
        )
        # new_activity.toc_item_id = theory_of_change.id

    # # Create a new record in the toc graph table
    # toc_item = TheoryOfChange()
    # toc_item.name = dto.name
    # toc_item.project_id = dto.prj_id
    # # TODO: make this optional
    # toc_item.type_id = 2  # id of the activity type
    # toc_item.from_id = None
    # toc_item.to_id = None
    # # TODO: make this optional
    # toc_item.sem_id = 1  # id of the sem type.
    # toc_item.description = dto.notes
    # # toc_item.theory_of_change_id = get_toc_by_project_id(dto.prj_id, db).id

    # db.add(toc_item)
    # db.commit()

    # # Update the activity with the toc_item id
    # new_activity.toc_item_id = toc_item.id
    # db.commit()

    # return ApiResponse(data=[record])
    return get_project_activities(new_activity.prj_id, db)


@router.get("/{projectId}", response_model=ApiResponse)
def get_activities(projectId: int, db: Session = Depends(models.get_db)):
    return get_project_activities(project_id=projectId, db=db)
