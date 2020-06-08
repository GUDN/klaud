from typing import List

from fastapi import UploadFile


def extract_content_type(file_parts: List[UploadFile]) -> str:
    content_types = set(
        part.content_type for part in file_parts
        if part.content_type
    )
    if len(content_types) == 0:
        return None
    elif len(content_types) == 1:
        return tuple(content_types)[0]
    else:
        raise ValueError('multiply content types')
