from fastapi import Depends, FastAPI

from . import auth, database
from .routes import fs, master, root, system

app = FastAPI(
    title='KLAUD',
    version='0.1.0',
    description='Base cloud storage',
    docs_url='/_docs',
    redoc_url=None,
    on_startup=[
        database.init,
        auth.init
    ]
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
app.include_router(
    master.router,
    prefix='/_master',
    tags=['master'],
    dependencies=[Depends(auth.auths(auth.Scopes.MASTER))]
)
app.include_router(
    fs.router,
    tags=['fs']
)
