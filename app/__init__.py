import logging

from fastapi import FastAPI

from .api_v1 import api as api_v1
from .middleware.correlation_request_id import CorrelationRequestIDMiddleware
from .middleware.logging import LogTransactionMiddleware, SimpleAuthLoggingMiddleware
from .utils.auth import APITokens


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

APITokens.register_token('ABC', 'ABC Token')

app = FastAPI()
app.mount('/api/v1', api_v1)

app.add_middleware(LogTransactionMiddleware)
app.add_middleware(SimpleAuthLoggingMiddleware)
app.add_middleware(CorrelationRequestIDMiddleware)
