from typing import Optional

from pydantic import BaseModel, Field

from klaud.types.path import Path


class File_(BaseModel):
    path: Path = Field(..., description='Full path to file', example='/path/to/file')
    owner: str = Field(..., description='Owner username', example='john_doe')
    length: int = Field(..., description='File size in bytes', example=100)
    content_type: Optional[str] = Field(..., example='text/plain')
