from pydantic import BaseModel, Field

from klaud.database import ping

from .router import router


class HealthState(BaseModel):
    core: bool = Field(..., description='core state', example=True)
    database: bool = Field(..., description='database connection state', example=True)


@router.get(
    '/health',
    summary='Check system health',
    response_model=HealthState,
)
async def health_check():
    return HealthState(
        core=True,
        database=await ping()
    )
