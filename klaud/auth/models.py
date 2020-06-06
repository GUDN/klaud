from typing import Optional

from pydantic import BaseModel, Field, validator

from klaud.models.user import UserInDB

from .scopes import Scopes


class Token(BaseModel):
    access_token: str = Field(..., example='simple_access_token')
    token_type: str = Field(..., example='Bearer')


class AuthObject(BaseModel):
    user: UserInDB
    scope: Scopes


class UpdateForm(BaseModel):
    username: Optional[str] = Field(None, example='john_doe')
    password: Optional[str] = None

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
