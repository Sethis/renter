

from fastapi import FastAPI

from .routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI(title="Simbir.GO", version="0.0.2a", description="Like the yandex taxi but..", on_startup=)

    init_routers(app)
    app.

    return app
