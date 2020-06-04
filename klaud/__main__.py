import uvicorn

from .settings import settings


def main():
    uvicorn.run(
        'klaud:app',
        port=settings.port,
        host=settings.host,
        reload=settings.hot_reload
    )


if __name__ == '__main__':
    main()
