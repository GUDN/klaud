from fastapi.responses import PlainTextResponse

from . import register, status  # noqa: F401
from .router import router


@router.get(
    '/',
    summary='Check master permissions',
    response_class=PlainTextResponse
)
def check_master():
    return 'you are master'
