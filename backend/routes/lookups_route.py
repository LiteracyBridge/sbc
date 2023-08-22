import models
from dataclass_wizard import asdict, fromdict
from fastapi import APIRouter, Depends, HTTPException
from models import LuAccessType, LuIndiKit, LuCountry, LuImportance
from schema import ApiResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/indi-kit")
def get_indicator_types(db: Session = Depends(models.get_db)):
    data = db.query(LuIndiKit).all()

    return ApiResponse(data=data)


@router.get("")
def get_data(db: Session = Depends(models.get_db)):
    access_types = db.query(LuAccessType).all()
    countries = db.query(LuCountry).all()
    indikit = db.query(LuIndiKit).all()
    importance = db.query(LuImportance).all()

    return ApiResponse(
        data=[
            {
                "access_types": access_types,
                "countries": countries,
                "indi_kit": indikit,
                "importance": importance,
            }
        ]
    )
