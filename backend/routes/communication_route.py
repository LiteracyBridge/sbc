from typing import Optional, List

import models
from fastapi import APIRouter, Depends
from models import AccessRequest, Communication
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session, subqueryload

router = APIRouter()


class CommunicationDto(BaseModel):
    project_id: int
    message_objectives: str
    delivery_platforms: Optional[str]
    format: Optional[str]
    key_points: Optional[str]
    contents: Optional[str]
    target_audiences: List[int]
    indicators: List[int]


@router.get("/{project_id}", response_model=ApiResponse)
def find_all(project_id: int, db: Session = Depends(models.get_db)):
    results = (
        db.query(Communication)
        .filter(Communication.project_id == project_id)
        .options(
            subqueryload(Communication.target_audiences).subqueryload(
                Communication.indicators
            )
        )
        .all()
    )

    return ApiResponse(data=results)


@router.post("/", response_model=ApiResponse)
def create(dto: CommunicationDto, db: Session = Depends(models.get_db)):
    item: CommunicationDto = CommunicationDto()
    item.project_id = dto.project_id
    item.message_objectives = dto.message_objectives
    item.format = dto.format

    db.add(item)
    db.commit()

    return ApiResponse(
        data=db.query(Communication)
        .filter(Communication.project_id == dto.project_id)
        .all()
    )
