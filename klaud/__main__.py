import uvicorn

from . import app
from .settings import settings


def main():
    uvicorn.run(
        app,
        port=settings.port,
        host=settings.host
    )


if __name__ == '__main__':
    main()
