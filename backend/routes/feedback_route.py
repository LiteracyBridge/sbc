from pydantic import BaseModel
from typing import Annotated
import models
from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, File, Form, UploadFile
from models import LuIndiKit
from schema import ApiResponse
from sqlalchemy.orm import Session

router = APIRouter()


class FeedbackDto(BaseModel):
    type: str
    title: str
    description: str
    editing_user_id: int


@router.post("")
def create_feedback(
    # dto: FeedbackDto,
    files: list[UploadFile],
    db: Session = Depends(models.get_db),
):
    # print(dto)
    print({"filenames": [file.filename for file in files]})

    return {
        "filenames": [file.filename for file in files],
        "size": [file.size for file in files],
    }

    # return ApiResponse(data=data)
