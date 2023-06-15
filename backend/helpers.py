from typing import Any
from pydantic import BaseModel
from db_models.project import TheoryOfChange
from fastapi import Depends
from sqlalchemy.orm import Session


class ToCItemDto(BaseModel):
    project_id: int
    type: str
    name: str
    reference: Any


def get_toc_by_project_id(projectId: int, db: Session):
    record = (
        db.query(TheoryOfChange).filter(TheoryOfChange.project_id == projectId).first()
    )
    return record


def create_toc_item(dto: ToCItemDto, db: Session):
    toc_item: TheoryOfChange = TheoryOfChange()
    toc_item.name = dto.name
    toc_item.from_id = None
    toc_item.to_id = None
    toc_item.description = ''
    toc_item.project_id = dto.project_id
    # toc_item.theory_of_change_id = get_toc_by_project_id(dto.project_id, db).id
    # TODO: make this optional
    toc_item.sem_id = 1  # id of the sem type.

    if dto.type == "activity":
        toc_item.type_id = 2
    if dto.type == "objective" or dto.type == "outcome":
        toc_item.type_id = 4

    db.add(toc_item)
    db.commit()
    db.refresh(toc_item)

    # Update the activity with the toc_item id
    dto.reference.toc_item_id = toc_item.id
    db.commit()

    return toc_item
