from dataclasses import dataclass
from typing import Generic, Any, List, TypeVar
from pydantic import BaseModel, ConfigDict
from fastapi.encoders import jsonable_encoder


T = TypeVar("T")


class ApiResponse:
    # model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    data: List[Any] = []

    def __init__(self, data: List[T]):
        self.data = jsonable_encoder(data)

    # class Config:
    #     from_attributes = True
