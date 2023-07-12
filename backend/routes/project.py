from typing import List, Optional, Dict, Annotated

from sqlalchemy import text
from models import LuDriver, ProjectDriver
from helpers import ToCItemDto, create_toc_item

import models
from fastapi import APIRouter, Depends, HTTPException, Body
from models import ProjectData
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session

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
    record = db.query(models.Project).filter(models.Project.id == id).first()

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


# Project objectives route
@router.get("/{project_id}/data", response_model=ApiResponse)
def get_project_data(project_id: int, db: Session = Depends(models.get_db)):
    return ApiResponse(
        data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
    )


@router.post("/{project_id}/data", response_model=ApiResponse)
def update_data(
    project_id: int, dto: ProjectObjectiveDto, db: Session = Depends(models.get_db)
):
    """Manage project objectives"""

    # Remove deleted objectives
    if len(dto.removed) > 0:
        db.query(ProjectData).filter(ProjectData.id.in_(dto.removed)).delete()

    # Update existing objectives
    if len(dto.updated) > 0:
        for item in dto.updated:
            [value] = item.values()
            [key] = item.keys()

            record = db.query(ProjectData).filter(ProjectData.id == int(key)).first()

            if record is None:
                continue

            # FIXME: Update corresponding theory of change item
            record.data = value
            db.commit()

    # Create new objectives
    if len(dto.added) > 0:
        for item in dto.added:
            record: ProjectData = ProjectData()
            record.q_id = 10
            record.data = item
            record.module = dto.module
            record.name = dto.name
            record.prj_id = project_id
            record.editing_user_id = dto.editing_user_id

            db.add(record)
            db.commit()
            db.refresh(record)

            if dto.module == "objectives":
                # Create theory of change objective item
                toc = create_toc_item(
                    ToCItemDto(
                        project_id=project_id,
                        name=item,
                        reference=record,
                        type="objective",
                    ),
                    db=db,
                )

                record.theory_of_change_id = toc.id
                db.commit()

    return ApiResponse(
        data=db.query(ProjectData).filter(ProjectData.prj_id == project_id).all()
    )


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
