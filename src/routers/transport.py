

from fastapi import APIRouter

from src.di.shortcuts import database, current_user
from src.types.transport import FullTransport, WriteTransport, UserWriteTransport, EditTransport
from src.exceptions.transport import undefined_transport, its_not_user_transport, undefined_type
from src.enums.transport import TransportTypes


transport_controller_router = APIRouter(tags=["TransportController"])


@transport_controller_router.get("/api/Transport/{id}")
async def get_tranpost_by_id(id: int, db: database) -> FullTransport:
    if not await db.check_transport_is_exist(id):
        raise undefined_transport

    return await db.get_transport_by_id(id)


@transport_controller_router.post("/api/Transport")
async def add_new_transport(
        transport: UserWriteTransport,
        db: database,
        user: current_user
) -> FullTransport:
    if transport.transportType not in TransportTypes.get_write_types():
        raise undefined_type

    transport = WriteTransport(ownerId=user.id, **transport.__dict__)

    return await db.add_transport(transport)


@transport_controller_router.put("/api/Transport/{id}")
async def edit_personal_transport(
        id: int,
        transport: EditTransport,
        db: database,
        user: current_user
) -> FullTransport:

    if not await db.check_transport_is_exist(id):
        raise undefined_transport

    current_transport = await db.get_transport_by_id(ido=id)

    if current_transport.ownerId != user.id:
        raise its_not_user_transport

    return await db.edit_transport(transport, transport_id=id)


@transport_controller_router.delete("/api/Transport/{id}")
async def delete_transport(id: int, db: database, user: current_user) -> dict[str, bool]:
    if not await db.check_transport_is_exist(id):
        raise undefined_transport

    current_transport = await db.get_transport_by_id(ido=id)

    if current_transport.ownerId != user.id:
        raise its_not_user_transport

    await db.delete_transport(id)

    return {"ok": True}
