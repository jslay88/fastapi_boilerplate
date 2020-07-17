import logging
from typing import Optional
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


logger = logging.getLogger(__name__)

security = HTTPBearer()


@dataclass
class APITokens:
    _tokens = []

    @classmethod
    def register_token(cls, token: str, description: str):
        cls._tokens.append({
            'token': token,
            'description': description
        })

    @classmethod
    def remove_token(cls, token: str):
        cls._tokens = [t for t in cls._tokens if t['token'] != token]

    @classmethod
    def validate_token(cls, token: str) -> Optional[dict]:
        for _token in cls._tokens:
            if token.lower() == _token['token'].lower():
                return _token


def get_authorized_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = APITokens.validate_token(credentials.credentials)
    if not token:
        logger.warning(f'Unauthorized attempt with token: {credentials.credentials}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized',
        )
    logger.info(f'Request Authorized: {token["description"]}')
    return token
