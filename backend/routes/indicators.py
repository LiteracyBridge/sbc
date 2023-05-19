from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from schema import ApiResponse
import models


router = APIRouter()


@router.get("/types", response_model=ApiResponse)
def get_indicator_types(db: Session = Depends(models.get_db)):
    data = db.query(models.IndicatorType).all()

    return ApiResponse(data=data)


@router.get("/", response_model=ApiResponse)
def get_indicator(db: Session = Depends(models.get_db)):
    data = db.query(models.Indicator).all()

    return ApiResponse(data=data)
