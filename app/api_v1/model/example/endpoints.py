import logging
from typing import Optional

from fastapi import Depends, Header

from . import router
from .models import ExampleRequest, ExampleResponse
from ....utils.auth import get_authorized_user


logger = logging.getLogger(__name__)


@router.post('/predict', response_model=ExampleResponse)
async def example_prediction(
    request: ExampleRequest,
    X_Correlation_ID: Optional[str] = Header(None),
    X_Request_ID: Optional[str] = Header(None),
    token: str = Depends(get_authorized_user)
):
    """
    Make a prediction against the Example Model

    This is useful because blah
    * A
    * B
    * C
    """
    return dict(base_response_field_1='OK Base Response')
