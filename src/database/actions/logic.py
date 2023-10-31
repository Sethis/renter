

import math
from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.types.user import StandartUserWithId, BaseUser
from src.types.transport import FullTransport, WriteTransport, BaseTransport
from src.types.rent import FullRent, StandartRent
from src.enums.rent import PriceTypes
from src.database.actions import usecases
from src.factories.converter import (
    get_converted_db_model_to_pydantic_model,
    get_converted_sequence_of_db_model_to_pydantic_model_list
)
from src.enums.transport import TransportTypesWithAll


class Logic:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_unactive_token(self, token: str):
        """
        This add a token to the unactive tokens list
        WARNING put token in the list only with caution
        :param token: value of unactive token
        :return: nothing
        """
        await usecases.add_unactive_token(token, session=self._session)
        await self._session.commit()

    async def check_token_is_active(self, token: str) -> bool:
        """
        Get boolean value. True if the token is active, False if the token unactive
        :param token: the search value
        :return: boolean
        """
        token = await usecases.get_unactive_token(token, session=self._session)

        return token is None

    async def add_user(self, user: BaseUser) -> StandartUserWithId:
        """
        Add a new user to the database by pydantic object user
        :param user: abstract pydantic object
        :return: user object that will create
        """

        result = await usecases.add_new_user(user, session=self._session)

        await self._session.commit()

        return get_converted_db_model_to_pydantic_model(result, StandartUserWithId)

    async def update_user(
            self,
            user: BaseUser,
            hash_password: bool = True,
            user_id: Optional[int] = None
    ) -> StandartUserWithId:
        """
        Replace a current database user with a user object that will passed
        :param user_id: By this value will search in the database.
        If it is None, user_id will get from user.id(if it exist)
        :param user: The user object that will replace current user in the database
        :param hash_password: This params responsible for user.password needs hash or not.
        WARNING! Disable it only when a password in the user.password already has been hashed
        if you don't want security issues or some other problems
        :return: The pydantic user object convert from a User database model
        """

        result = await usecases.update_user(
            user,
            session=self._session,
            hash_password=hash_password,
            user_id=user_id
        )

        await self._session.commit()

        return get_converted_db_model_to_pydantic_model(result, StandartUserWithId)

    async def get_user_by_id(self, user_id: int) -> StandartUserWithId:
        """
        It get a user from database by its id and convert this to pydantic user object
        :param user_id: By this value will search in the database
        :return: The pydantic user object convert from a User database model
        """
        result = await usecases.get_user_by_id(user_id, session=self._session)

        return get_converted_db_model_to_pydantic_model(result, StandartUserWithId)

    async def get_user_by_name(self, user_name: str) -> StandartUserWithId:
        """
        It get a user from database by his name and convert this to pydantic user object
        :param user_name: By this value will search in the database
        :return: The pydantic user object convert from a User database model
        """
        result = await usecases.get_user_by_name(user_name, session=self._session)

        return get_converted_db_model_to_pydantic_model(result, StandartUserWithId)

    async def check_username_is_exists(self, user_name: str, editing_user_id: Optional[str] = None) -> bool:
        """
        Check that a user with this username is exist and return result
        :param editing_user_id: If passed, it wiil check that different user have a name or not
        :param user_name: By this value will search in the database
        :return: boolean data that mean a user is exist or not
        """
        result = await usecases.get_user_by_name(user_name, session=self._session)

        if result is None:
            return False

        if result.id == editing_user_id:
            return False

        return True

    async def check_user_is_exists(self, user_id: int) -> bool:
        """
        Check that a user with this id is exist and return result
        :param user_id: By this value will search in the database
        :return: boolean data that mean a user is exist or not
        """
        result = await usecases.get_user_by_id(user_id, session=self._session)

        if result is None:
            return False

        return True

    async def delete_user_by_id(self, user_id: int):
        """
        Delete a user by his id
        :param user_id: By this value will search in the database
        :return: nothing
        """
        await usecases.delete_user(user_id, session=self._session)
        await self._session.commit()

    async def get_all_users(self, start: int, count: int) -> list[StandartUserWithId]:
        """
        This will give an all users by the offset and the limit
        WARNING! Monitor only admin access to this functionality
        :param start: The offset of users
        :param count: The limit a users per result
        :return: The list of users(may be with lenght equality 0)
        """
        users = await usecases.get_all_users(offset=start, limit=count, session=self._session)

        return get_converted_sequence_of_db_model_to_pydantic_model_list(
            users, StandartUserWithId
        )

    async def get_all_transports(
            self,
            start: int,
            count: int,
            transport_type: TransportTypesWithAll
    ) -> list[FullTransport]:
        """
        Get all transports in a pydantic objects
        :param start: The offset of transport
        :param count: The limit a transport per result
        :param transport_type: values from TransportTypesWithAll enums
        :return: The list of transports(may be with lenght equality 0)
        """

        transports = await usecases.get_all_transports(
            offset=start,
            limit=count,
            transport_type=transport_type,
            session=self._session
        )

        return get_converted_sequence_of_db_model_to_pydantic_model_list(
            transports, FullTransport
        )

    async def get_transport_by_id(self, ido: int) -> FullTransport:
        """
        Get transport object by its id
        :param ido: transport id
        :return: Pydantic transport object
        """

        transport = await usecases.get_transport_by_id(ido, session=self._session)

        return get_converted_db_model_to_pydantic_model(transport, FullTransport)

    async def check_transport_is_exist(self, ido: int) -> bool:
        """
        Get a boolean value. If a transport with this id exist, return True
        :param ido: transport id
        :return: boolean
        """

        transport = await usecases.get_transport_by_id(ido, session=self._session)

        return transport is not None

    async def add_transport(self, transport: WriteTransport) -> FullTransport:
        """
        This add the transport to the databse and return its object
        :param transport: a pydantic object. Add to database
        :return: new transport pydantic object
        """
        transport = await usecases.add_transport(transport, session=self._session)
        await self._session.commit()

        return get_converted_db_model_to_pydantic_model(transport, FullTransport)

    async def edit_transport(
            self,
            transport: BaseTransport,
            transport_id: Optional[int] = None
    ) -> FullTransport:

        """
        This edit the transport to the databse and return its object
        :param transport_id: this will be use if the transport havent id value
        :param transport: a pydantic object. Edit current database
        :return: new transport pydantic object
        """
        transport = await usecases.edit_transport(
            transport,
            session=self._session,
            transport_id=transport_id)
        await self._session.commit()

        return get_converted_db_model_to_pydantic_model(transport, FullTransport)

    async def delete_transport(self, transport_id: int):
        """
        Delete a transport with this id from the database
        :param transport_id: id of transport that will be delete
        :return: nothing
        """
        await usecases.delete_transport_by_id(transport_id, session=self._session)

        await self._session.commit()

    async def get_transport_by_radius(
            self,
            lat: float,
            long: float,
            radius: float,
            transport_type: TransportTypesWithAll
    ) -> list[FullTransport]:
        """
        Get a transport by a current user place and a radius
        :param transport_type: one of a transport type from the TransportTypesWithAll enum
        :param lat: user's latitude data
        :param long:  user's longitude data
        :param radius: search radius
        :return: The list of transports in the radius(may be with lenght equality 0)
        """

        transports = await usecases.get_transport_by_radius(
            lat=lat,
            long=long,
            radius=radius,
            transport_type=transport_type,
            session=self._session
        )

        return get_converted_sequence_of_db_model_to_pydantic_model_list(
            transports, FullTransport
        )

    async def get_rent_by_id(self, rent_id: int) -> FullRent:
        """
        Get a pydantic rent object by its id
        :param rent_id:  id of search rent
        :return: pydantic object of rent
        """

        rent = await usecases.get_rent_by_id(rent_id, session=self._session)

        return get_converted_db_model_to_pydantic_model(rent, FullRent)

    async def get_rents_by_user_id(self, user_id: int) -> list[FullRent]:
        """
        Get a rent objects by id of its owner
        :param user_id: id of rent owner
        :return: The list of rents(may be with lenght equality 0)
        """

        rents = await usecases.get_rents_by_user_id(user_id, session=self._session)

        return get_converted_sequence_of_db_model_to_pydantic_model_list(
            rents, FullRent
        )

    async def get_rents_by_transport_id(self, transport_id: int) -> list[FullRent]:
        """
        Get a rent objects by id of its transport
        :param transport_id: id of rent's transport
        :return: The list of rents(may be with lenght equality 0)
        """

        rents = await usecases.get_rents_by_transport_id(transport_id, session=self._session)

        return get_converted_sequence_of_db_model_to_pydantic_model_list(
            rents, FullRent
        )

    async def add_rent(self, rent: StandartRent) -> FullRent:
        """
        Add a rent model to a database and return its from the database
        :param rent: The pydantic rent object which will add to the database
        :return: A pydantic model of a new rent
        """

        rent = await usecases.add_rent(rent, session=self._session)
        await self._session.commit()

        return get_converted_db_model_to_pydantic_model(
            rent, FullRent
        )

    async def edit_rent(self, rent: StandartRent, rent_id: Optional[int] = None) -> FullRent:
        """
        Edit a rent model in a database and return its from the database
        :param rent_id: if rent object havent a id, will use rent_id
        :param rent: The pydantic rent object which will replace current rent
        :return: A pydantic model of a new rent
        """

        rent = await usecases.edit_rent(rent, session=self._session, rent_id=rent_id)
        await self._session.commit()

        return get_converted_db_model_to_pydantic_model(
            rent, FullRent
        )

    async def check_rent_is_exist(self, ido: int) -> bool:
        """
        Get a boolean value. If a rent with this id exist, return True
        :param ido: rent id
        :return: boolean
        """

        rent = await usecases.get_rent_by_id(ido, self._session)

        return rent is not None

    async def check_transport_is_busy(self, ido: int) -> bool:
        """
        Check rent is current busy
        :param ido: transport id
        :return: boolean
        """

        return await usecases.get_transport_is_busy(ido, session=self._session)

    async def check_rent_is_alredy_finish(self, rent_id: int) -> bool:
        """
        Check rent is alredy finish and return result
        :param rent_id: rent id
        :return: boolean
        """

        rent = await usecases.get_rent_by_id(rent_id, session=self._session)

        return rent.timeEnd is not None

    @staticmethod
    def _get_price(td: timedelta, rent: StandartRent) -> float:
        if rent.priceType == PriceTypes.DAYS:
            return (td.days + 1) * rent.priceOfUnit

        elif rent.priceType == PriceTypes.MINUTES:
            minutes = math.ceil(td.seconds / 60)
            return minutes * rent.priceOfUnit

        raise ValueError("undefined price type")

    async def finish_rent(self, rent_id: int) -> FullRent:
        """
        Finish the rent by rent id
        :param rent_id: id of current rent
        :return:
        """

        rent = await self.get_rent_by_id(rent_id)

        current_time = datetime.now()
        delta = current_time - rent.timeStart

        price = self._get_price(delta, rent)

        rent = StandartRent(
            transportId=rent.transportId,
            userId=rent.userId,
            timeStart=rent.timeStart,
            timeEnd=datetime.now(),
            priceOfUnit=rent.priceOfUnit,
            priceType=rent.priceType,
            finalPrice=price
        )

        new_rent = await self.edit_rent(rent, rent_id=rent_id)

        user = await self.get_user_by_id(rent.userId)

        user.balance -= price

        await self.update_user(user, hash_password=False)

        await self._session.commit()

        return new_rent

    async def delete_rent_by_id(self, rent_id: int):
        await usecases.delete_rent_by_id(rent_id, session=self._session)

        await self._session.commit()
