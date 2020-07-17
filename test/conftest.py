import pytest
from fastapi.testclient import TestClient

from app import create_app
from app.utils.auth import APITokens


@pytest.fixture()
def unit_test_client():
    yield TestClient(create_app())


@pytest.fixture()
def valid_auth_token_header():
    token = {
        'token': 'Test',
        'description': 'Test Token'
    }
    APITokens.register_token(**token)
    yield {
        'Authorization': f'Bearer {token["token"]}'
    }
    APITokens.remove_token(token['token'])


@pytest.fixture()
def invalid_auth_token_header():
    return {
        'Authorization': 'Bearer Test'
    }
