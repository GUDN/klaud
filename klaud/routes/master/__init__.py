from fastapi import Depends
from fastapi.responses import PlainTextResponse

from klaud.auth import AuthObject, Scopes, auths

from . import register  # noqa: F401
from .router import router


@router.get(
    '/',
    summary='Check master permissions',
    response_class=PlainTextResponse
)
def check_master(curr: AuthObject = Depends(auths(Scopes.MASTER))):
    return 'you are master'
