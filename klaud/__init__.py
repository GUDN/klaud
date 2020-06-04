from fastapi import FastAPI

from .routes import root, system

app = FastAPI()

app.include_router(root.router)
app.include_router(
    system.router,
    prefix='/_sys',
    tags=['system']
)
