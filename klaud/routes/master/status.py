from fastapi import HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, validator

from klaud.models.user import UserInDB

from .router import router


class MasterStatusForm(BaseModel):
    target: str = Field(
        ...,
        description='target\'s username',
        example='john_doe'
    )
    status: bool = Field(..., description='new status')

    @validator('target')
    def target_has_length(cls, v):
        v = v.strip()
        if not len(v):
            raise ValueError('cannot be zero length')
        return v


@router.put(
    '/manage',
    summary='Manage master status for accounts',
    response_class=PlainTextResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Target is not exists'
        }
    }
)
async def manage(form: MasterStatusForm):
    user = await UserInDB.find_by_username(form.target)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Target not found'
        )
    user.is_master = form.status
    await user.insert()
    return 'OK'
