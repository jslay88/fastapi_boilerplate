from pydantic import Field

from ..models import BaseModelRequest, BaseModelResponse


class ExampleRequest(BaseModelRequest):
    a_number_field_1: int
    a_number_field_2: int = Field(..., gt=10)


class ExampleResponse(BaseModelResponse):
    pass
