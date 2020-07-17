import logging

from ...middleware.logging import get_auth_description
from ...middleware.correlation_request_id import get_correlation_id, get_request_id


class AuthDescriptionFilter(logging.Filter):
    def filter(self, record):
        record.auth_description = get_auth_description()
        return True


class CorrelationRequestIDFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        record.request_id = get_request_id()
        return True
