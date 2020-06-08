from fastapi import Depends, HTTPException, status
from fastapi.responses import PlainTextResponse

from klaud.auth import AuthObject, Scopes, auths
from klaud.database import gfs
from klaud.types.path import Path

from .router import router


@router.delete(
    '/{path:path}',
    summary='Delete file (requires write scope)',
    response_class=PlainTextResponse,
    responses={
        404: {
            'description': 'File not found'
        }
    }
)
async def delete(path: Path = '', curr: AuthObject = Depends(auths(Scopes.WRITE))):
    filename = f'@{curr.user.username}{path}'
    gfs_ = gfs()
    deleted = False
    async for f in gfs_.find({'filename': filename}):
        await gfs_.delete(f._id)
        deleted = True
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Current path is not exists'
        )
    return 'OK'
