from typing import Optional, List

from pydantic import BaseModel, Field


class ModelListResponse(BaseModel):
    models: List[str]


class BaseModelRequest(BaseModel):
    field_1: str = Field(..., title='Field 1 Description')
    field_2: Optional[str] = Field(None, title='Field 2 Description', max_length=20)


class BaseModelResponse(BaseModel):
    base_response_field_1: str
