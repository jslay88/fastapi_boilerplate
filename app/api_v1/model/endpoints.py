import logging
from typing import Optional

from fastapi import Depends, Header

from . import router
from .models import ModelListResponse
from ...utils.auth import get_authorized_user


logger = logging.getLogger(__name__)


@router.get('', response_model=ModelListResponse)
async def model_list(
    X_Correlation_ID: Optional[str] = Header(None),
    X_Request_ID: Optional[str] = Header(None),
    _: str = Depends(get_authorized_user)
):
    return {'models': [
        'example'
    ]}
