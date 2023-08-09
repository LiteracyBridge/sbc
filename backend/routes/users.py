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


class UpdateUserDto(BaseModel):
    name: Optional[str]
    sms: Optional[str]
    whatsapp: Optional[str]
    address_as: Optional[str]


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


@router.get("/organisation/{email}", response_model=ApiResponse)
def get_org_users(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    print(user)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    data = db.query(User).filter(User.organisation_id == user.organisation_id).all()

    return ApiResponse(data=data)


@router.get("/{email}", response_model=ApiResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    if email is None:
        raise HTTPException(status_code=400, detail="Email is required")

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.organisation_id is None:
        # If the user is not associated with an organisation, check if they have an invitation
        # and if so, associate them with the organisation
        invitation = db.query(Invitation).filter(Invitation.email == email).first()

        if invitation is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.organisation_id = invitation.organisation_id
        db.commit()
        db.refresh(user)

    return ApiResponse(data=[user])


@router.put("/{id}", response_model=ApiResponse)
def update_user(id: int, dto: UpdateUserDto, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if dto.name is not None:
        user.name = dto.name
    if dto.address_as is not None:
        user.address_as = dto.address_as
    if dto.sms is not None:
        user.sms = dto.sms
    if dto.whatsapp is not None:
        user.whatsapp = dto.whatsapp

    db.commit()
    return ApiResponse(data=[user])
