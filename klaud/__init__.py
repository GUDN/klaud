from fastapi import FastAPI

from . import auth
from .routes import root, system

app = FastAPI(
    title='KLAUD',
    version='0.1.0',
    description='Base cloud storage',
    docs_url='/_docs',
    redoc_url=None
)

app.include_router(root.router)
app.include_router(
    auth.router,
    tags=['authentication']
)
app.include_router(
    system.router,
    prefix='/_sys',
    tags=['system']
)
