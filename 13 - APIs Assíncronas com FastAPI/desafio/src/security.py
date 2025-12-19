import time
from uuid import uuid4
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

import os

SECRET = os.getenv("JWT_SECRET", "my-secret")  
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: int
    iat: int
    nbf: int
    jti: str


class JWTToken(BaseModel):
    access_token: str


def sign_jwt(user_id: int) -> JWTToken:
    now = int(time.time())
    payload = {
        "iss": "desafio-bank.com.br",
        "sub": user_id,
        "aud": "desafio-bank",
        "exp": now + 1800, 
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return JWTToken(access_token=token)


def decode_jwt(token: str) -> Optional[AccessToken]:
    try:
        decoded = jwt.decode(
            token, SECRET, audience="desafio-bank", algorithms=[ALGORITHM]
        )
        return AccessToken(**decoded)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )
            token_data = decode_jwt(credentials.credentials)
            if not token_data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token.",
                )
            return token_data
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization credentials not provided.",
        )


async def get_current_user(
    token: AccessToken = Depends(JWTBearer()),
) -> dict:
    return {"user_id": token.sub}