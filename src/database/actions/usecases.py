

from typing import Coroutine, Any, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, Select
from sqlalchemy.dialects.postgresql import insert

from src.database.structure.model import User, Transport, UnactiveToken, Rent
from src.types.user import BaseUser
from src.types.transport import WriteTransport, BaseTransport
from src.types.rent import StandartRent
from src.encryption.password import get_password_hash
from src.enums.transport import TransportTypesWithAll


def add_unactive_token(token: str, session: AsyncSession) -> Coroutine[Any, Any, Any]:
    stmt = insert(UnactiveToken).values(token=token)
    stmt = stmt.on_conflict_do_nothing()

    return session.execute(stmt)


def get_unactive_token(token: str, session: AsyncSession) -> Coroutine[Any, Any, UnactiveToken | None]:
    stmt = select(UnactiveToken).where(UnactiveToken.token == token)

    return session.scalar(stmt)


def add_new_user(user: BaseUser, session: AsyncSession) -> Coroutine[Any, Any, User]:
    password = get_password_hash(user.password)

    balance = user.get_balance()
    is_admin = user.get_admin_status()

    stmt = insert(User).values(
        username=user.username,
        password=password,
        isAdmin=is_admin,
        balance=balance
    )

    stmt = stmt.returning(User)

    return session.scalar(stmt)


def get_user_by_id(user_id: int, session: AsyncSession) -> Coroutine[Any, Any, User]:
    stmt = select(User).where(User.id == user_id)

    return session.scalar(stmt)


def get_user_by_name(user_name: str, session: AsyncSession) -> Coroutine[Any, Any, User]:
    stmt = select(User).where(User.username == user_name)

    return session.scalar(stmt)


def update_user(
        user: BaseUser,
        session: AsyncSession,
        hash_password: bool = True,
        user_id: Optional[int] = None
) -> Coroutine[Any, Any, User]:

    if hash_password:
        password = get_password_hash(user.password)

    else:
        password = user.password

    if user_id is None:
        user_id = user.get_id()

    balance = user.get_balance()
    is_admin = user.get_admin_status()

    stmt = update(User).where(User.id == user_id).values(
        username=user.username,
        password=password,
    )

    if user.get_balance_is_exists():
        stmt = stmt.values(balance=balance)

    if user.get_admin_status_is_exists():
        stmt = stmt.values(isAdmin=is_admin)

    stmt = stmt.returning(User)

    return session.scalar(stmt)


def delete_user(user_id, session: AsyncSession) -> Any:
    stmt = delete(User).where(User.id == user_id)

    return session.execute(stmt)


async def get_all_users(offset: int, limit: int, session: AsyncSession) -> Sequence[User]:
    stmt = select(User).offset(offset).limit(limit)

    result = await session.scalars(stmt)

    return result.all()


async def get_all_transports(
        offset: int,
        limit: int,
        transport_type: TransportTypesWithAll,
        session: AsyncSession
) -> Sequence[Transport]:

    stmt = select(Transport).offset(offset).limit(limit)

    if transport_type != TransportTypesWithAll.ALL:
        stmt = stmt.where(Transport.transportType == transport_type)

    result = await session.scalars(stmt)
    return result.all()


def get_transport_by_id(transport_id: int, session: AsyncSession) -> Coroutine[Any, Any, Transport]:
    stmt = select(Transport).where(Transport.id == transport_id)

    return session.scalar(stmt)


def add_transport(transport: WriteTransport, session: AsyncSession) -> Coroutine[Any, Any, Transport]:
    stmt = insert(Transport).values(
        ownerId=transport.ownerId,
        canBeRented=transport.canBeRented,
        transportType=transport.transportType,
        model=transport.model,
        color=transport.color,
        identifier=transport.identifier,
        description=transport.description,
        latitude=transport.latitude,
        longitude=transport.longitude,
        minutePrice=transport.minutePrice,
        dayPrice=transport.dayPrice
    )

    stmt = stmt.returning(Transport)

    return session.scalar(stmt)


def edit_transport(
        transport: BaseTransport,
        session: AsyncSession,
        transport_id: Optional[int] = None
) -> Coroutine[Any, Any, Transport]:

    if transport_id is None:
        transport_id = transport.get_transport_id()

    stmt = update(Transport).values(
        canBeRented=transport.canBeRented,
        model=transport.model,
        color=transport.color,
        identifier=transport.identifier,
        description=transport.description,
        latitude=transport.latitude,
        longitude=transport.longitude,
        minutePrice=transport.minutePrice,
        dayPrice=transport.dayPrice
    )

    stmt = stmt.where(Transport.id == transport_id)

    if transport.get_owner_id_is_exist():
        stmt = stmt.values(ownerId=transport.get_owner_id())

    if transport.get_transport_type_is_exist():
        stmt = stmt.values(transportType=transport.get_transport_type())

    stmt = stmt.returning(Transport)

    return session.scalar(stmt)


def delete_transport_by_id(transport_id: int, session: AsyncSession) -> Any:
    stmt = delete(Transport).where(Transport.id == transport_id)

    return session.execute(stmt)


def get_id_of_free_transport() -> Select:
    all_busy_transports_id = select(Rent.transportId).where(Rent.timeEnd.is_(None))
    all_finish_transport = Transport.id.not_in(all_busy_transports_id)

    can_be_ranted = Transport.canBeRented.is_(True)

    stmt = select(Transport.id).where(
        all_finish_transport,
        can_be_ranted
    )

    return stmt


async def get_transport_by_radius(
        lat: float,
        long: float,
        radius: float,
        transport_type: TransportTypesWithAll,
        session: AsyncSession
) -> Sequence[Transport]:
    free_transport_stmt = get_id_of_free_transport()

    stmt = select(Transport)

    left = func.pow(Transport.latitude - lat, 2)
    right = func.pow(Transport.longitude - long, 2)
    check = left + right <= radius ** 2

    stmt = stmt.where(
        check,
        Transport.id.in_(free_transport_stmt)
    )

    if transport_type != TransportTypesWithAll.ALL:
        stmt = stmt.where(Transport.transportType == transport_type)
        
    result = await session.scalars(stmt)

    return result.all()


async def get_transport_is_busy(tranport_id: int, session: AsyncSession) -> bool:
    free_transport_stmt = get_id_of_free_transport()

    result = await session.scalars(free_transport_stmt)

    return tranport_id not in result.all()


def get_rent_by_id(rent_id: int, session: AsyncSession) -> Coroutine[Any, Any, Rent]:
    stmt = select(Rent).where(Rent.id == rent_id)

    return session.scalar(stmt)


async def get_rents_by_user_id(user_id: int, session: AsyncSession) -> Sequence[Rent]:
    stmt = select(Rent).where(Rent.userId == user_id)

    result = await session.scalars(stmt)

    return result.all()


async def get_rents_by_transport_id(transport_id: int, session: AsyncSession) -> Sequence[Rent]:
    stmt = select(Rent).where(Rent.transportId == transport_id)

    result = await session.scalars(stmt)

    return result.all()


def add_rent(rent: StandartRent, session: AsyncSession) -> Coroutine[Any, Any, Rent]:
    stmt = insert(Rent).values(
        transportId=rent.transportId,
        userId=rent.userId,
        timeStart=rent.timeStart,
        timeEnd=rent.timeEnd,
        priceOfUnit=rent.priceOfUnit,
        priceType=rent.priceType,
        finalPrice=rent.finalPrice
    )

    stmt = stmt.returning(Rent)

    return session.scalar(stmt)


def edit_rent(
        rent: StandartRent,
        session: AsyncSession,
        rent_id: Optional[int] = None
) -> Coroutine[Any, Any, Rent]:

    stmt = update(Rent)
    stmt = stmt.values(
        transportId=rent.transportId,
        userId=rent.userId,
        timeStart=rent.timeStart,
        timeEnd=rent.timeEnd,
        priceOfUnit=rent.priceOfUnit,
        priceType=rent.priceType,
        finalPrice=rent.finalPrice
    )

    stmt = stmt.where(Rent.id == rent_id)

    stmt = stmt.returning(Rent)

    return session.scalar(stmt)


def delete_rent_by_id(rent_id: int, session: AsyncSession) -> Any:
    stmt = delete(Rent).where(Rent.id == rent_id)

    return session.execute(stmt)
