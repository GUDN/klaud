import asyncio
from typing import List

from fastapi import Depends, File, HTTPException, UploadFile, status

from klaud.auth import AuthObject, Scopes, auths
from klaud.database import gfs
from klaud.models.file import File_
from klaud.types.path import Path
from klaud.utils.fs import extract_content_type

from .router import router


@router.put(
    '/{path:path}',
    summary='Updoad file (requires write scope)',
    status_code=status.HTTP_201_CREATED,
    response_model=File_
)
async def put(
    path: Path = '',
    file_parts: List[UploadFile] = File(...),
    curr: AuthObject = Depends(auths(Scopes.WRITE))
):
    try:
        content_type = extract_content_type(file_parts)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Different content types'
        )
    filename = f'@{curr.user.username}{path}'
    gfs_ = gfs()
    await asyncio.gather(*[
        gfs_.delete(f['_id'])
        for f in await gfs_.find({'filename': filename}).to_list(None)
    ])
    gin = gfs_.open_upload_stream(
        filename,
        metadata={
            'content_type': content_type
        }
    )
    for part in file_parts:
        await gin.write(part.file)
    await gin.close()
    return File_(
        path=path,
        owner=curr.user.username,
        length=gin.length,
        content_type=content_type
    )
