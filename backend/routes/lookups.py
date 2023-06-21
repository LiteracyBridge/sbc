import models
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from models import LuIndiKit
from schema import ApiResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/indi-kit", response_model=ApiResponse)
def get_indicator_types(db: Session = Depends(models.get_db)):
    data = db.query(LuIndiKit).all()

    return ApiResponse(data=data)
