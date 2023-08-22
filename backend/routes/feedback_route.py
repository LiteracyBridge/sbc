from copy import deepcopy
from pydantic import BaseModel
from typing import Annotated, Optional
import models
from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, File, Form, UploadFile
from models import Feedback, User
from schema import ApiResponse
from sqlalchemy.orm import Session
import boto3
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    files: list[UploadFile] = [],
    db: Session = Depends(models.get_db),
):
    feedback: Feedback = Feedback()
    feedback.type = type
    feedback.title = title
    feedback.description = description
    feedback.user_id = editing_user_id

    # Upload files to S3
    temp_files = deepcopy(files)
    # feedback.files = upload_to_s3(files, "sbc-upload", "feedbacks")
    print(feedback.files)

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    # TODO: Send email to admin
    # Send email to support
    #

    user = db.query(User).filter(User.id == editing_user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    msg = MIMEMultipart()
    msg["Subject"] = f"New Feedback: {title}"
    msg["From"] = user.email
    msg["To"] = "lawrence@amplio.org"

    # Set message body
    body = MIMEText(
        f"""Hello Team,

        {user.address_as} has submitted new feedback. See below for details.

        Title: {title}
        Issue Type: {feedback.type}
        Description: {description}

        {'Attached are the files submitted' if len(temp_files) > 0 else ''}
        """,
        "plain",
    )
    msg.attach(body)

    # Attach files
    for f in temp_files:
        part = MIMEApplication(f.file.read())
        part.add_header(
            "Content-Disposition", "attachment", filename=f.filename
        )
        msg.attach(part)

    ses_client = boto3.client("ses")
    ses_client.send_raw_email(
        Destinations=["lawrence@amplio.org"],
        RawMessage={"Data": msg.as_string()}
    )

    return ApiResponse(data=[feedback])
