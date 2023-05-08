from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from schema import ApiResponse
from models import User, get_db
import models


router = APIRouter()


@router.get("/", response_model=ApiResponse)
def get_users(db: Session = Depends(get_db)):
    data = db.query(models.User).filter().all()

    return ApiResponse(data=data)
