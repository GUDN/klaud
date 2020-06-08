from fastapi import Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from gridfs.errors import NoFile

from klaud.auth import AuthObject, Scopes, auths
from klaud.database import gfs
from klaud.types.path import Path

from .router import router


@router.get(
    '/{path:path}',
    summary='Download file (requires read scope)',
    response_class=StreamingResponse,
    responses={
        404: {
            'description': 'File not found'
        }
    }
)
async def get(path: Path = '', curr: AuthObject = Depends(auths(Scopes.READ))):
    filename = f'@{curr.user.username}{path}'
    try:
        gout = await gfs().open_download_stream_by_name(filename)
    except NoFile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Current path is not exists'
        )

    async def _handler():
        while (chunk := await gout.read(4096)):
            yield chunk

    return StreamingResponse(
        _handler(),
        media_type=gout.metadata['content_type']
    )
