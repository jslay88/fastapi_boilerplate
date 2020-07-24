import json
import logging
from io import StringIO

import pytest
from fastapi.testclient import TestClient

from app import create_app
from app.utils.auth import APITokens
from app.utils.log.formatters import APIJSONFormatter
from app.utils.log.filters import AuthDescriptionFilter, CorrelationRequestIDFilter


class LogCapture(StringIO):
    def __iter__(self):
        pos = self.tell()
        self.seek(0, 0)
        line = self.readline()
        while line:
            yield json.loads(line.strip())
            line = self.readline()
        self.seek(pos)

    def __len__(self):
        return self.tell()

    def __getitem__(self, item):
        pos = self.tell()
        self.seek(item.start)
        line = self.readline()
        while line:
            yield json.loads(line.strip())
            if item.stop and item.stop >= self.tell():
                self.seek(pos)
                return
            if item.step and item.step > 1:
                self.readlines(item.step - 1)
            line = self.readline()
        self.seek(pos)


@pytest.fixture()
def unit_test_client():
    yield TestClient(create_app())


@pytest.fixture()
def valid_auth_token():
    token = {
        'token': 'Test',
        'description': 'Test Token'
    }
    APITokens.register_token(**token)
    yield token
    APITokens.remove_token(token['token'])


@pytest.fixture()
def valid_auth_token_header(valid_auth_token):
    yield {
        'Authorization': f'Bearer {valid_auth_token["token"]}'
    }


@pytest.fixture()
def invalid_auth_token():
    return {
        'token': 'Bad Token',
        'description': 'Bad Token'
    }


@pytest.fixture()
def invalid_auth_token_header(invalid_auth_token):
    return {
        'Authorization': f'Bearer {invalid_auth_token["token"]}'
    }


@pytest.fixture()
def log_capture():
    log_stream = LogCapture()
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=log_stream)
    handler.setFormatter(APIJSONFormatter())
    handler.addFilter(AuthDescriptionFilter())
    handler.addFilter(CorrelationRequestIDFilter())
    logger.addHandler(handler)
    yield log_stream
