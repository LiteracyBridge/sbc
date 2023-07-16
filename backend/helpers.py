from typing import Any, Optional, List
from pydantic import BaseModel
from models import TheoryOfChange
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session
import boto3
from botocore.exceptions import ClientError
import os
import sentry_sdk


class ToCItemDto(BaseModel):
    project_id: int
    type: str
    name: str
    reference: Optional[Any]


def get_toc_by_project_id(projectId: int, db: Session):
    record = (
        db.query(TheoryOfChange).filter(TheoryOfChange.project_id == projectId).first()
    )
    return record


def create_toc_item(dto: ToCItemDto, db: Session):
    toc_item: TheoryOfChange = TheoryOfChange()
    toc_item.name = dto.name
    toc_item.from_id = None
    toc_item.to_id = None
    toc_item.description = ""
    toc_item.project_id = dto.project_id
    # toc_item.theory_of_change_id = get_toc_by_project_id(dto.project_id, db).id
    # TODO: make this optional
    toc_item.sem_id = 1  # id of the sem type.

    if dto.type == "activity":
        toc_item.type_id = 2
    if dto.type == "objective" or dto.type == "outcome":
        toc_item.type_id = 4

    db.add(toc_item)
    db.commit()
    db.refresh(toc_item)

    # Update the activity with the toc_item id
    if dto.reference is not None:
        dto.reference.theory_of_change_id = toc_item.id
        db.commit()

    return toc_item


def upload_to_s3(files: list[UploadFile], bucket_name, folder_name=None) -> List[str]:
    s3_client = boto3.client("s3")
    file_urls: List[str] = []

    for f in files:
        object_name = f.filename

        if folder_name is not None:
            object_name = f"{folder_name}/{f.filename}"

        try:
            s3_client.upload_fileobj(f.file, bucket_name, object_name)

            # Get the url of the uploaded file
            bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)
            object_url = f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{bucket_name}/{object_name}"
            file_urls.append(object_url)

        except ClientError as e:
            print(e)
            sentry_sdk.capture_exception(e)

    return file_urls
