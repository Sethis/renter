

from typing import Coroutine, Any, Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

from src.database.structure.model import User, Transport
from src.types.user import BaseUser
from src.types.transport import WriteTransport, BaseTransport
from src.encryption.password import get_password_hash


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
        active: Optional[bool] = None,
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

    if active is not None:
        stmt = stmt.values(active=active)

    stmt = stmt.returning(User)

    return session.scalar(stmt)


def delete_user(user_id, session: AsyncSession):
    stmt = delete(User).where(User.id == user_id)

    return session.execute(stmt)


async def get_all_users(offset: int, limit: int, session: AsyncSession) -> Sequence[User]:
    stmt = select(User).offset(offset).limit(limit)

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

    if transport.get__transport_type_is_exist():
        stmt = stmt.values(transportType=transport.get_transport_type())

    stmt = stmt.returning(Transport)

    return session.scalar(stmt)


def delete_transport_by_id(transport_id: int, session: AsyncSession):
    stmt = delete(Transport).where(Transport.id == transport_id)

    return session.scalar(stmt)
