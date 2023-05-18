from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from schema import ApiResponse
from models import Indicator, get_db
import models


router = APIRouter()


@router.get("/", response_model=ApiResponse)
def get_indicator_types(db: Session = Depends(get_db)):
    data = db.query(models.Indicator).all()

    return ApiResponse(data=data)
