from typing import Optional
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session
from schema import ApiResponse
from models import Invitation, Organisation, User, get_db


router = APIRouter()


class UserDto(BaseModel):
    email: str
    name: Optional[str]
    last_project_id: Optional[int]


@router.post("/", response_model=ApiResponse)
def create(dto: UserDto, db: Session = Depends(get_db)):
    invite = db.query(Invitation).filter(Invitation.email == dto.email).first()

    if invite is None:
        return HTTPException(status_code=400, detail="Account cannot be created")

    user: User = User()
    user.email = dto.email
    user.name = dto.name
    user.organisation_id = invite.organisation_id
    user.last_project_id = dto.last_project_id

    db.add(user)
    db.commit()
    db.refresh(user)

    return ApiResponse(data=[user])


@router.get("/", response_model=ApiResponse)
def get_users(email: Optional[str], db: Session = Depends(get_db)):
    if email is None:
        raise HTTPException(status_code=400, detail="Email is required")

    user = db.query(User).filter(User.email == email).first()
    print(user)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.organisation_id is None:
        # TODO: try to update user's organisation id if not set
        return ApiResponse(data=[])
        # raise HTTPException(status_code=404, detail="User not found")

    data = db.query(User).filter(User.organisation_id == user.organisation_id).all()

    print(user)

    return ApiResponse(data=data)
