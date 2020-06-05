from pydantic import BaseModel, Field

from klaud.models.user import UserInDB


class Token(BaseModel):
    access_token: str = Field(..., example='simple_access_token')
    token_type: str = Field(..., example='Bearer')


class AuthObject(BaseModel):
    user: UserInDB