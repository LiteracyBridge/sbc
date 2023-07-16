from pydantic import BaseModel
from typing import Annotated
import models
from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, File, Form, UploadFile
from models import Feedback
from schema import ApiResponse
from sqlalchemy.orm import Session

from helpers import upload_to_s3

router = APIRouter()


class FeedbackDto(BaseModel):
    type: str
    title: str
    description: str
    editing_user_id: int


@router.post("")
def create_feedback(
    type: Annotated[str, Form()],
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    editing_user_id: Annotated[int, Form()],
    files: list[UploadFile],
    db: Session = Depends(models.get_db),
):
    feedback: Feedback = Feedback()
    feedback.type = type
    feedback.title = title
    feedback.description = description
    feedback.user_id = editing_user_id

    # Upload files to S3
    feedback.files = upload_to_s3(files, "sbc-upload", "feedbacks")
    print(feedback.files)

    db.add(feedback)
    db.commit()

    return ApiResponse(data=[feedback])
