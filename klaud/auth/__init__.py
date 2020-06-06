from datetime import datetime, timedelta
from typing import Callable

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from pymongo.errors import DuplicateKeyError

from klaud.models.user import User, UserInDB
from klaud.settings import settings
from klaud.utils import passwords

from .models import AuthObject, Token, UpdateForm
from .scopes import Scopes

ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/_token",
    scopes={
        'master': 'master priviliges on token (avaliable only for master account)',
        'manage': 'manage current account'
    }
)
router = APIRouter()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


async def init():
    master = UserInDB(
        uid='',
        username=settings.master_name,
        hashed=passwords.hashpw(settings.master_password),
        is_master=True
    )
    await master.insert()


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
    scopes = credentials.scopes
    scope = Scopes.NONE
    if scopes:
        if 'master' in scopes and not user.is_master:
            raise credentials_exception
        for scope_ in scopes:
            scope_ = Scopes.__members__.get(scope_.upper())
            if scope_:
                scope |= scope_
    return Token(
        access_token=generate_token({
            'username': user.username,
            'scope': scope.value
        }),
        token_type='bearer'
    )


async def auth(token: str = Depends(oauth2_scheme)) -> AuthObject:
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
    return AuthObject(
        user=user,
        scope=Scopes(payload.get('scope', 0))
    )


def auths(scope: Scopes = Scopes.NONE) -> Callable[[AuthObject], AuthObject]:
    def _auths(obj: AuthObject = Depends(auth)) -> AuthObject:
        if scope is Scopes.NONE:
            return obj
        elif (scope & obj.scope).value:
            return obj
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token scope error',
        )
    return _auths


@router.get(
    '/_me',
    summary='Get info about current user',
    response_model=User
)
def get_me(curr: AuthObject = Depends(auth)):
    return User(**curr.user.dict())


@router.delete(
    '/_me',
    summary='Delete current account permanently (requires manage scope)',
    response_class=PlainTextResponse
)
async def delete_me(curr: AuthObject = Depends(auths(Scopes.MANAGE))):
    await curr.user.delete()
    return 'OK'


@router.patch(
    '/_me',
    summary='Update account (requires manage scope)',
    response_class=PlainTextResponse
)
async def patch_me(form: UpdateForm, curr: AuthObject = Depends(auths(Scopes.MANAGE))):
    user = curr.user
    if form.username:
        user.username = form.username
    if form.password:
        user.hashed = passwords.hashpw(form.password)
    try:
        await user.insert()
        return 'OK'
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username is not free'
        )
