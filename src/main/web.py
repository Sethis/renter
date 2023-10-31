

from fastapi import FastAPI

from src.main.routers import init_routers
from src.routers.start import init_models


def create_app() -> FastAPI:
    app = FastAPI(title="Simbir.GO", version="0.1.0", description="Like the yandex.GO but..", lifespan=init_models)

    init_routers(app)

    return app
