from typing import Optional

from sqlalchemy.sql import select

from models import get_db, Organisation, User, AccessRequest
from fastapi import APIRouter, Depends
from models import AccessRequest, User
from pydantic import BaseModel
from schema import ApiResponse
from sqlalchemy.orm import Session

router = APIRouter()


class AccessRequestDto(BaseModel):
    name: str
    notes: Optional[str]
    email: Optional[str]


@router.get("/{user_id}")
def get_org_details(user_id: int, db: Session = Depends(get_db)):
    org = (
        db.query(Organisation)
        .filter(
            Organisation.id.in_(
                select(db.query(User.organisation_id).filter(User.id == user_id).subquery())
            )
        )
        .first()
    )
    return ApiResponse(data=[org])


@router.post("/access-request")
def create(dto: AccessRequestDto, db: Session = Depends(get_db)):
    item: AccessRequest = AccessRequest()
    item.notes = dto.notes
    item.email = dto.email
    item.name = dto.name

    db.add(item)
    db.commit()

    return ApiResponse(data=[item])
