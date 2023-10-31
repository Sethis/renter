

from datetime import datetime

from fastapi import APIRouter

from src.di.shortcuts import database, current_user, rent_id_, transport_id_, rent_type_
from src.types.transport import FullTransport
from src.types.rent import FullRent, StandartRent
from src.exceptions.rent import (
    its_not_user_rent,
    rent_self_ransport,
    undefined_rent_type,
    transport_is_busy,
    rent_is_already_finish,
    its_not_your_rent,
    undefined_rent
)
from src.exceptions.transport import its_not_user_transport, undefined_transport
from src.enums.transport import TransportTypesWithAll
from src.enums.rent import PriceTypes


rent_controller_router = APIRouter(tags=["RentController"])


@rent_controller_router.get("/api/Rent/Transport")
async def get_rent_by_radius(
        lat: float,
        long: float,
        radius: float,
        type: TransportTypesWithAll,
        db: database
) -> list[FullTransport]:

    return await db.get_transport_by_radius(
        lat=lat,
        long=long,
        radius=radius,
        transport_type=type
    )


@rent_controller_router.get("/api/Rent/MyHistory")
async def get_current_user_history(
        db: database,
        user: current_user
) -> list[FullRent]:

    return await db.get_rents_by_user_id(user.id)


@rent_controller_router.get("/api/Rent/{rentId}")
async def get_rent_by_rent_id(
        rent_id: rent_id_,
        db: database,
        user: current_user
) -> FullRent:
    if not await db.check_rent_is_exist(rent_id):
        raise undefined_rent

    rent = await db.get_rent_by_id(rent_id)

    if rent.userId == user.id:
        return rent

    transport = await db.get_transport_by_id(rent.transportId)

    if transport.ownerId == user.id:
        return rent

    raise its_not_user_rent


@rent_controller_router.get("/api/Rent/TransportHistory/{transportId}")
async def get_transports_rent_history(
        transport_id: transport_id_,
        db: database,
        user: current_user
) -> list[FullRent]:

    if not await db.check_transport_is_exist(transport_id):
        raise undefined_transport

    transport = await db.get_transport_by_id(transport_id)

    if transport.ownerId != user.id:
        raise its_not_user_transport

    return await db.get_rents_by_transport_id(transport_id)


@rent_controller_router.post("/api/Rent/New/{transportId}")
async def start_rent(
        transport_id: transport_id_,
        rent_type: rent_type_,
        db: database,
        user: current_user
) -> FullRent:

    if not await db.check_transport_is_exist(transport_id):
        raise undefined_transport

    if await db.check_transport_is_busy(transport_id):
        raise transport_is_busy

    transport = await db.get_transport_by_id(transport_id)

    if transport.ownerId == user.id:
        raise rent_self_ransport

    if rent_type == PriceTypes.DAYS:
        unit = transport.dayPrice

    elif rent_type == PriceTypes.MINUTES:
        unit = transport.minutePrice

    else:
        raise undefined_rent_type

    if unit is None:
        unit = 0

    rent = StandartRent(
        transportId=transport_id,
        userId=user.id,
        timeStart=datetime.now(),
        priceOfUnit=unit,
        priceType=rent_type,
    )

    return await db.add_rent(rent)


@rent_controller_router.post("/api/Rent/End/{rentId}")
async def finish_rent(
        rent_id: rent_id_,
        db: database,
        user: current_user
) -> FullRent:
    if not await db.check_rent_is_exist(rent_id):
        raise undefined_rent

    if await db.check_rent_is_alredy_finish(rent_id):
        raise rent_is_already_finish

    rent = await db.get_rent_by_id(rent_id)

    if rent.userId != user.id:
        raise its_not_your_rent

    return await db.finish_rent(rent_id)
