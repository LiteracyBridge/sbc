import models
from dataclass_wizard import asdict
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
    importance = db.query(LuImportance).all()

    # Map the indikit data to a dictionary, section -> sub_sector -> [indicators]
    indikit = {}
    results = db.query(LuIndiKit).all()
    for result in results:
        items = indikit.get(result.sector, [])
        items.append(result)
        indikit[result.sector] = items

    for key in indikit.keys():
        sub_sectors = {}

        for result in indikit[key]:
            items = sub_sectors.get(result.sub_sector, [])
            items.append(result)
            sub_sectors[result.sub_sector] = items

        indikit[key] = sub_sectors
        # indikit[result.sector] = asdict(result)


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
