import logging
from uuid import uuid4
from typing import Union
from contextvars import ContextVar

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


logger = logging.getLogger(__name__)


CORRELATION_ID_CTX_KEY = 'correlation_id'
REQUEST_ID_CTX_KEY = 'request_id'

_correlation_id_ctx_var: ContextVar[Union[str, None]] = ContextVar(CORRELATION_ID_CTX_KEY, default=None)
_request_id_ctx_var: ContextVar[Union[str, None]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_correlation_id():
    return _correlation_id_ctx_var.get()


def get_request_id():
    return _request_id_ctx_var.get()


class CorrelationRequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        correlation_id = _correlation_id_ctx_var.set(request.headers.get('X-Correlation-ID', None))
        request_id = _request_id_ctx_var.set(request.headers.get('X-Request-ID', str(uuid4())))

        response = await call_next(request)
        response.headers['X-Request-ID'] = get_request_id()
        if request.headers.get('X-Correlation-ID'):
            response.headers['X-Correlation-ID'] = get_correlation_id()

        _correlation_id_ctx_var.reset(correlation_id)
        _request_id_ctx_var.reset(request_id)

        return response
