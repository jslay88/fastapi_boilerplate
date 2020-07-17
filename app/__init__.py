import logging

from fastapi import FastAPI, Depends

from .api_v1 import api as api_v1
from .middleware.correlation_request_id import CorrelationRequestIDMiddleware
from .middleware.logging import LogTransactionMiddleware, SimpleAuthLoggingMiddleware
from .utils.auth import APITokens, get_authorized_user


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def create_app():
    APITokens.register_token('ABCABCABC', 'ABC Token')

    app = FastAPI()
    app.mount('/api/v1', api_v1)

    app.add_middleware(LogTransactionMiddleware)
    app.add_middleware(SimpleAuthLoggingMiddleware)
    app.add_middleware(CorrelationRequestIDMiddleware)

    @app.get('/health')
    def health(): return {'health': 'healthy'}

    @app.get('/auth_test')
    def auth_test(_: str = Depends(get_authorized_user)):
        return {'detail': 'OK'}

    return app
