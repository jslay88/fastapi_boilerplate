import logging
from typing import Union
from contextvars import ContextVar

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..utils.auth import APITokens


logger = logging.getLogger(__name__)


AUTH_DESCRIPTION_KEY = 'auth_description'

_auth_description_ctx_var: ContextVar[Union[dict, None]] = ContextVar(AUTH_DESCRIPTION_KEY, default=None)


def get_auth_description():
    return _auth_description_ctx_var.get()


class LogTransactionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        def log_request(r: Request):
            logger.info('Log Request', extra={
                'path': r.url.path,
                'headers': [(k, v if k != 'authorization' else f'{v[:12]}{"*" * (len(v) - 12)}')
                            for k, v in r.headers.items()]
            })

        def log_response(r: Response):
            logger.info('Log Response', extra={
                'headers': r.headers,
                'status_code': r.status_code
            })

        log_request(request)
        response = await call_next(request)
        log_response(response)
        return response


class SimpleAuthLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token = APITokens.validate_token(request.headers.get('Authorization', '').replace('Bearer ', ''))
        auth_description = _auth_description_ctx_var.set(
             token['description'] if token else None
        )

        response = await call_next(request)

        _auth_description_ctx_var.reset(auth_description)

        return response
