from fastapi import HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, validator
from pymongo.errors import DuplicateKeyError

from klaud.models.user import UserInDB
from klaud.utils import passwords

from .router import router


class RegisterForm(BaseModel):
    username: str = Field(..., example='john_doe')
    password: str = Field(..., description='initial password (can be changed)')
    is_master: bool = Field(False, description='initial master status')

    @validator('username')
    def username_has_length(cls, v):
        v = v.strip()
        if not len(v):
            raise ValueError('cannot be zero length')
        return v

    @validator('password')
    def password_has_length(cls, v):
        if not len(v):
            raise ValueError('cannot be zero length')
        return v


@router.post(
    '/register',
    summary='Register new user',
    response_class=PlainTextResponse,
    responses={
        status.HTTP_409_CONFLICT: {
            'description': 'Username conflict'
        }
    }
)
async def register(form: RegisterForm):
    user = UserInDB(
        **form.dict(),
        hashed=passwords.hashpw(form.password),
        uid=''
    )
    try:
        await user.insert_new()
        return 'OK'
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username is not free'
        )
