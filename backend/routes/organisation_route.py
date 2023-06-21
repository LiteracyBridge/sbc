from typing import Optional

import models
from fastapi import APIRouter, Depends
from models import AccessRequest
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session

router = APIRouter()


class AccessRequestDto(BaseModel):
    name: str
    notes: Optional[str]
    email: Optional[str]


@router.post("/access-request", response_model=ApiResponse)
def create(dto: AccessRequestDto, db: Session = Depends(models.get_db)):
    item: AccessRequest = AccessRequest()
    item.notes = dto.notes
    item.email = dto.email
    item.name = dto.name

    db.add(item)
    db.commit()

    return ApiResponse(data=[item])
