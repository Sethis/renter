

from fastapi import APIRouter

from src.di.shortcuts import database, admin_user, rent_id_, transport_id_, user_id_
from src.types.rent import StandartRent, FullRent
from src.exceptions.rent import (
    rent_is_already_finish,
    undefined_rent
)
from src.exceptions.user import user_is_undefined
from src.exceptions.transport import undefined_transport


admin_rent_controller_router = APIRouter(tags=["AdminRentController"])


@admin_rent_controller_router.get("/api/Rent/{rentId}")
async def get_rent_by_id(
        rent_id: rent_id_,
        db: database,
        _admin: admin_user
) -> FullRent:

    if not await db.check_rent_is_exist(rent_id):
        raise undefined_rent

    return await db.get_rent_by_id(rent_id)


@admin_rent_controller_router.get("/api/Admin/UserHistory/{userId}")
async def get_rents_by_user_id(
        user_id: user_id_,
        db: database,
        _admin: admin_user
) -> list[FullRent]:
    if not await db.check_user_is_exists(user_id):
        raise user_is_undefined

    return await db.get_rents_by_user_id(user_id)


@admin_rent_controller_router.get("/api/Admin/TransportHistory/{transportId}")
async def get_rents_by_transport_id(
        transport_id: transport_id_,
        db: database,
        _admin: admin_user
) -> list[FullRent]:

    if not await db.check_transport_is_exist(transport_id):
        raise undefined_transport

    return await db.get_rents_by_transport_id(transport_id)


@admin_rent_controller_router.post("/api/Admin/Rent")
async def add_new_rent(
        rent: StandartRent,
        db: database,
        _admin: admin_user
) -> FullRent:

    return await db.add_rent(rent)


@admin_rent_controller_router.post("/api/Admin/Rent/End/{rentId}")
async def finish_rent(
        rent_id: rent_id_,
        db: database,
        _admin: admin_user
) -> FullRent:
    if not await db.check_rent_is_exist(rent_id):
        raise undefined_transport

    if await db.check_rent_is_alredy_finish(rent_id):
        raise rent_is_already_finish

    return await db.finish_rent(rent_id)


@admin_rent_controller_router.put("/api/Admin/Rent/{id}")
async def edit_rent(
        id: int,
        rent: StandartRent,
        db: database,
        _admin: admin_user
) -> FullRent:

    return await db.edit_rent(rent, rent_id=id)


@admin_rent_controller_router.delete("/api/Admin/Rent/{rentId}")
async def delete_rent(
        rent_id: rent_id_,
        db: database,
        _admin: admin_user
) -> dict[str, bool]:
    if not await db.check_rent_is_exist(rent_id):
        raise undefined_transport

    await db.delete_rent_by_id(rent_id)

    return {"ok": True}
