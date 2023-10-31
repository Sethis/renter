

from typing import Annotated

from fastapi import APIRouter, Query

from src.di.shortcuts import database, admin_user
from src.types.transport import FullTransport, WriteTransport
from src.exceptions.transport import undefined_transport, undefined_type
from src.exceptions.user import user_is_undefined
from src.enums.transport import TransportTypes, TransportTypesWithAll

admin_transport_controller_router = APIRouter(tags=["AdminTransportController"])


@admin_transport_controller_router.get("/api/Admin/Transport")
async def get_all_transports(
        start: int,
        count: int,
        transport_type: Annotated[TransportTypesWithAll, Query(alias="transportType")],
        db: database,
        _admin: admin_user
) -> list[FullTransport]:

    return await db.get_all_transports(start, count, transport_type)


@admin_transport_controller_router.get("/api/Admin/Transport/{id}")
async def get_tranpost_by_id(id: int, db: database, _admin: admin_user) -> FullTransport:
    if not await db.check_transport_is_exist(id):
        raise undefined_transport

    return await db.get_transport_by_id(id)


@admin_transport_controller_router.post("/api/Admin/Transport")
async def add_new_transport(transport: WriteTransport, db: database, _admin: admin_user) -> FullTransport:
    if transport.transportType not in TransportTypes.get_write_types():
        raise undefined_type

    if not await db.check_user_is_exists(transport.ownerId):
        raise user_is_undefined

    return await db.add_transport(transport)


@admin_transport_controller_router.put("/api/Admin/Transport/{id}")
async def edit_transport(
        id: int,
        transport: WriteTransport,
        db: database,
        _admin: admin_user
) -> FullTransport:

    if transport.transportType not in TransportTypes.get_write_types():
        raise undefined_type

    if not await db.check_transport_is_exist(id):
        raise undefined_transport

    if not await db.check_user_is_exists(transport.ownerId):
        raise user_is_undefined

    return await db.edit_transport(transport, transport_id=id)


@admin_transport_controller_router.delete("/api/Admin/Transport/{id}")
async def delete_transport(id: int, db: database, _admin: admin_user) -> dict[str, bool]:
    if not await db.check_transport_is_exist(id):
        raise undefined_transport

    await db.delete_transport(id)

    return {"ok": True}
