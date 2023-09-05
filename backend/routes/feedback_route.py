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
import shutil
import base64

# from helpers import upload_to_s3

router = APIRouter()


class FeedbackDto(BaseModel):
    type: str
    title: str
    description: str
    editing_user_id: int
    files: list[str] = []


@router.post("")
def create_feedback(
    dto: FeedbackDto,
    db: Session = Depends(models.get_db),
):
    # image_data = base64.b64decode(dto.files[0])
    # with open("/tmp/image.jpg", "wb") as f:
    #     f.write(image_data)

    feedback: Feedback = Feedback()
    feedback.type = dto.type
    feedback.title = dto.title
    feedback.description = dto.description
    feedback.user_id = dto.editing_user_id

    # Upload files to S3
    # temp_files = deepcopy(files)
    # feedback.files = upload_to_s3(files, "sbc-upload", "feedbacks")
    # print(feedback.files)

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    # TODO: Send email to admin
    # Send email to support
    #

    user = db.query(User).filter(User.id == dto.editing_user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"New Feedback: {dto.title}"
    msg["From"] = user.email
    msg["To"] = "lawrence@amplio.org"

    # Set message body
    body = MIMEText(
        f"""Hello Team,

    {user.address_as} has submitted new feedback. See below for details.

    Title: {dto.title}
    Issue Type: {feedback.type}
    Description: {dto.description}

    {'Attached are the files submitted' if len(dto.files) > 0 else ''}
    """,
        "plain",
    )
    msg.attach(body)

    # Attach files
    for (index, f) in enumerate(dto.files):
        # print(f)

        file_location = f"/tmp/uploaded_file_{index}.jpg"
        image_data = base64.b64decode(f)
        with open(file_location, "wb") as file:
            file.write(image_data)
        # f.file.seek(0)

        # with open(file_location, "wb+") as file_object:
        #     shutil.copyfileobj(f.file, file_object)
        #     # file_object.write(f.file.read())

        part = MIMEApplication(open(file_location, "rb").read())
        part.add_header("Content-Disposition", "attachment", filename=f"file_{index}.jpg")
        msg.attach(part)

    ses_client = boto3.client("ses")
    ses_client.send_raw_email(
        Destinations=["lawrence@amplio.org"], RawMessage={"Data": msg.as_string()}
    )

    return ApiResponse(data=[feedback])
