from typing import List, Optional, Dict, Annotated
from datetime import datetime
from sqlalchemy import text
from models import LuDriver, ProjectDriver, Stakeholder, TheoryOfChange, get_db
from helpers import ToCItemDto, create_toc_item

import models
from fastapi import APIRouter, Depends, HTTPException, Body, Request, Response
from models import ProjectData, Project
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, subqueryload
from routes.theory_of_change import delete_toc_item
from model_events import delete_project_data

router = APIRouter()


# Types
class UpdateProjectDto(BaseModel):
    evaluation_strategy: Optional[str]
    feedback_strategy: Optional[str]
    sustainability_strategy: Optional[str]


class ProjectObjectiveDto(BaseModel):
    name: str
    module: str
    editing_user_id: int
    updated: List[Dict[str, str]] = []
    added: Optional[List[str]] = []
    removed: Optional[List[int]] = []


@router.get("/{id}", response_model=ApiResponse)
def find_project(id: int, db: Session = Depends(models.get_db)):
    record = (
        db.query(Project)
        .filter(Project.id == id)
        .options(subqueryload(Project.stakeholders), subqueryload(Project.organisation))
        .first()
    )

    if record is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return ApiResponse(data=[record])


@router.put("/{id}", response_model=ApiResponse)
def update_strategy(
    id: int, dto: UpdateProjectDto, db: Session = Depends(models.get_db)
):
    record = db.query(models.Project).filter(models.Project.id == id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # record.name = dto.name
    record.evaluation_strategy = dto.evaluation_strategy
    record.feedback_strategy = dto.feedback_strategy
    record.sustainability_strategy = dto.sustainability_strategy

    db.commit()
    db.refresh(record)

    return ApiResponse(data=[record])


## ================== PROJECT DRIVERS ================== ##
def get_project_drivers(project_id: int, db: Session = Depends(models.get_db)):
    """Returns a list of drivers for a project"""
    return db.query(ProjectDriver).filter(ProjectDriver.prj_id == project_id).all()


def driver_exists_in_project(
    project_id: int, driver_id: int, db: Session = Depends(models.get_db)
):
    """Check if driver exists in project"""

    return (
        db.query(ProjectDriver)
        .filter(
            ProjectDriver.lu_driver_id == driver_id,
            ProjectDriver.prj_id == project_id,
        )
        .first()
    ) is not None


@router.get("/drivers/{project_id}")
def get_project_drivers_with_interventions(
    project_id: int, db: Session = Depends(models.get_db)
):
    """Get list project drivers"""

    statement = text(
        """
    SELECT ld.id AS lu_id,
        ld.parent_id,
        ld.category_id,
        ld.name,
        ld.intervention_ids,
        dp.id AS dip_id,
        dp.prj_id
    FROM lu_drivers ld
    INNER JOIN drivers_in_prj dp ON
        ld.id = dp.lu_driver_id
         AND dp.prj_id = :project_id
         AND ld.intervention_ids IS NOT NULL;
        """
    )

    drivers = db.execute(statement, {"project_id": project_id}).all()
    return ApiResponse(data=[row._asdict() for row in drivers])


@router.post("/{project_id}/drivers")
def add_driver_to_project(
    project_id: int,
    lu_driver_id: Annotated[int, Body()],
    editing_user_id: Annotated[int, Body()],
    importance_id: Annotated[int, Body()] = 1,
    db: Session = Depends(models.get_db),
):
    """
    Add a driver to a project

    If the driver has a parent, add the parent driver to the project as well.
    """

    # If driver already exists in project, return
    if driver_exists_in_project(project_id=project_id, driver_id=lu_driver_id, db=db):
        return ApiResponse(
            data=get_project_drivers(project_id=project_id, db=db),
        )

    driver: LuDriver | None = (
        db.query(LuDriver).filter(LuDriver.id == lu_driver_id).first()
    )

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    new_driver: ProjectDriver = ProjectDriver()
    new_driver.lu_driver_id = driver.id
    new_driver.editing_user_id = editing_user_id
    new_driver.prj_id = project_id
    new_driver.importance_id = importance_id
    new_driver.notes_context = None
    new_driver.notes_gap = None
    new_driver.notes_goal = None

    db.add(new_driver)
    db.commit()

    # If parent driver is not None, add the parent driver to the project
    if driver.parent_id is not None or driver.parent_id != 0:
        if driver_exists_in_project(
            project_id=project_id, driver_id=driver.parent_id, db=db
        ):
            return ApiResponse(
                data=get_project_drivers(project_id=project_id, db=db),
            )

        parent = (
            db.query(ProjectDriver).filter(ProjectDriver.id == driver.parent_id).first()
        )

        if parent is not None:
            return ApiResponse(
                data=db.query(ProjectDriver)
                .filter(ProjectDriver.prj_id == project_id)
                .all()
            )

        parent = db.query(LuDriver).filter(LuDriver.id == driver.parent_id).first()

        if parent is None:
            raise HTTPException(status_code=404, detail="Parent driver not found")

        new_parent: ProjectDriver = ProjectDriver()
        new_parent.lu_driver_id = parent.id
        new_parent.editing_user_id = editing_user_id
        new_parent.prj_id = project_id
        new_parent.name = parent.name
        new_parent.notes_context = None
        new_parent.notes_gap = None
        new_parent.notes_goal = None

        db.add(new_parent)
        db.commit()

    return ApiResponse(
        data=get_project_drivers(project_id=project_id, db=db),
    )


## ================== END PROJECT DRIVERS ================== ##


# ===== START: PROJECT DATA ===== #
class ProjectDataDto(BaseModel):
    id: Optional[int]
    q_id: Optional[int]
    data: Optional[str]
    module: Optional[str]
    name: Optional[str]
    editing_user_id: Optional[int]


# Project objectives route
@router.get("/{project_id}/data", response_model=ApiResponse)
def get_project_data(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
    )


@router.post("/{project_id}/data", response_model=ApiResponse)
@router.put("/{project_id}/data", response_model=ApiResponse)
def update_or_create_data(
    project_id: int,
    dto: ProjectDataDto,
    db: Session = Depends(get_db),
):
    """Add or update project data"""

    record = ProjectData()
    is_new = True

    if dto.id is not None:
        _temp: ProjectData | None = (
            db.query(ProjectData).filter(ProjectData.id == dto.id).first()
        )

        if _temp is not None:
            is_new = False
            record = _temp

    record.q_id = dto.q_id
    record.data = dto.data
    record.module = dto.module
    record.name = dto.name
    record.prj_id = project_id
    record.editing_user_id = dto.editing_user_id

    if is_new:
        db.add(record)

    db.commit()
    db.refresh(record)

    # Update or create toc item
    if dto.module == "objectives" and is_new and dto.data is not None:
        # Create theory of change objective item
        toc = TheoryOfChange()
        toc.name = dto.data
        toc.links_to = []
        toc.sem_id = None
        toc.description = None
        toc.project_id = project_id
        toc.is_validated = False
        toc.type_id = 4

        db.add(toc)
        db.commit()
        db.refresh(toc)

        record.theory_of_change_id = toc.id
        db.commit()
        db.refresh(record)
    elif (
        dto.module == "objectives"
        and not is_new
        and record.theory_of_change_id is not None
    ):
        # Update theory of change objective item
        toc = (
            db.query(TheoryOfChange)
            .filter(TheoryOfChange.id == record.theory_of_change_id)
            .first()
        )
        toc.name = dto.data
        db.commit()

    db.refresh(record)
    return ApiResponse(data=[record])


@router.delete("/{project_id}/data/{id}", response_model=ApiResponse)
def delete_project_data_item(
    project_id: int,
    id: int,
    db: Session = Depends(get_db),
):
    item: ProjectData | None = (
        db.query(ProjectData).filter(ProjectData.id == id).first()
    )

    if item is None:
        return ApiResponse(data=[])

    # If project data is an objective, delete corresponding theory of change item
    if item.theory_of_change_id is not None:
        delete_toc_item(project_id=project_id, item_id=item.theory_of_change_id, db=db)

    delete_project_data(item_id=item.id, db=db)

    return ApiResponse(data=[item])


# ===== END: PROJECT DATA ===== #


# ================== START: PROJECT STAKEHOLDERS ================== ##
class StakeholderDto(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    sms: Optional[str]
    whatsapp: Optional[str]
    email: Optional[str]
    editing_user_id: int


def get_stakeholders(
    project_id: int, db: Session = Depends(models.get_db)
) -> ApiResponse:
    return ApiResponse(
        data=db.query(Stakeholder).filter(Stakeholder.project_id == project_id).all()
    )


@router.delete("/{project_id}/stakeholders/{stakeholder_id}")
def delete_stakeholder(
    project_id: int, stakeholder_id: int, db: Session = Depends(models.get_db)
) -> ApiResponse:
    """Delete a stakeholder from the project"""

    record: Stakeholder | None = (
        db.query(Stakeholder)
        .filter(Stakeholder.id == stakeholder_id, Stakeholder.project_id == project_id)
        .first()
    )

    if record is None:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    record.delete()
    db.commit()

    return get_stakeholders(project_id=project_id, db=db)


@router.post("/{project_id}/stakeholders")
def update_or_add_stakeholder(
    project_id: int, dto: StakeholderDto, db: Session = Depends(models.get_db)
) -> ApiResponse:
    """Add a new stakeholder to the project"""

    record: Stakeholder = Stakeholder()

    if dto.id is not None:
        temp = db.query(Stakeholder).filter(Stakeholder.id == dto.id).first()

        if temp is None:
            raise HTTPException(status_code=404, detail="Stakeholder not found")
        record = temp
    else:
        record.project_id = project_id
        record.created_at = datetime.now()

    record.name = dto.name
    record.description = dto.description
    record.sms = dto.sms
    record.whatsapp = dto.whatsapp
    record.email = dto.email
    record.editing_user_id = dto.editing_user_id
    record.updated_at = datetime.now()

    db.add(record)
    db.commit()

    return get_stakeholders(project_id=project_id, db=db)


# ================== END: PROJECT STAKEHOLDERS ==================== ##

# @router.post("/{project_id}/audience", response_model=ApiResponse)
# def update_audience(
#     project_id: int, dto: ProjectObjectiveDto, db: Session = Depends(models.get_db)
# ):
#     """Manage project audiences"""

#     # Remove deleted audiences
#     if len(dto.removed) > 0:
#         db.query(ProjectData).filter(ProjectData.id.in_(dto.removed)).delete()

#     # Update existing audiences
#     if len(dto.updated) > 0:
#         for item in dto.updated:
#             [value] = item.values()
#             [key] = item.keys()

#             record = db.query(ProjectData).filter(ProjectData.id == int(key)).first()

#             if record is None:
#                 continue

#             record.data = value
#             db.commit()

#     # Create new objectives
#     if len(dto.added) > 0:
#         for item in dto.added:
#             record: ProjectData = ProjectData()
#             record.q_id = 3
#             record.data = item
#             record.module = "audiences"
#             record.name = "secondary_audiences"
#             record.prj_id = project_id
#             record.editing_user_id = dto.editing_user_id

#             db.add(record)
#             db.commit()

#     return ApiResponse(
#         data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
#     )
