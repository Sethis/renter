

from fastapi import FastAPI

from src.routers.account import account_controller_router
from src.routers.admin_account import admin_account_controller_router
from src.routers.payments import payments_controller_router
from src.routers.transport import transport_controller_router
from src.routers.admin_transport import admin_transport_controller_router
from src.routers.rent import rent_controller_router
from src.routers.admin_rent import admin_rent_controller_router


def init_routers(app: FastAPI):
    app.include_router(account_controller_router)
    app.include_router(admin_account_controller_router)
    app.include_router(payments_controller_router)
    app.include_router(transport_controller_router)
    app.include_router(admin_transport_controller_router)
    app.include_router(rent_controller_router)
    app.include_router(admin_rent_controller_router)
