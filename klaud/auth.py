from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from pydantic import BaseModel, Field

from .models.user import User, UserInDB
from .settings import settings
from .utils import passwords

ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/_token")
router = APIRouter()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


class Token(BaseModel):
    access_token: str = Field(..., example='simple_access_token')
    token_type: str = Field(..., example='Bearer')


class AuthObject(BaseModel):
    user: UserInDB


def generate_token(payload: dict) -> str:
    payload.update({
        'exp': datetime.utcnow() + timedelta(minutes=settings.access_token_life)
    })
    return jwt.encode(
        payload,
        settings.secret,
        algorithm=ALGORITHM
    ).decode()


@router.post(
    '/_token',
    summary='generate access token',
    response_model=Token,
    responses={
        401: {
            'description': 'Invalid auth credentials'
        }
    }
)
async def login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await UserInDB.find_by_username(credentials.username)
    if not user:
        raise credentials_exception
    if not passwords.checkpw(credentials.password, user.hashed):
        raise credentials_exception
    return Token(
        access_token=generate_token({'username': user.username}),
        token_type='bearer'
    )


async def auth(token: str = Depends(oauth2_scheme)) -> UserInDB:
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[ALGORITHM])
    except PyJWTError:
        raise credentials_exception
    username = payload.get('username')
    if not username:
        raise credentials_exception
    user = await UserInDB.find_by_username(username)
    if not user:
        raise credentials_exception
    return AuthObject(user=user)


@router.get(
    '/_me',
    summary='Get info about current user',
    response_model=User
)
def me(curr: AuthObject = Depends(auth)):
    return User(**curr.user.dict())
