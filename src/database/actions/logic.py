

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.types.user import UserWithActive, StandartUserWithId, BaseUser
from src.database.actions import usecases
from src.factories.user import get_converted_db_user_to_pydantic_model


class Logic:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_user(self, user: BaseUser) -> StandartUserWithId:
        """
        Add a new user to the database by pydantic object user
        :param user: abstract pydantic object
        :return: user object that will create
        """

        result = await usecases.add_new_user(user, session=self._session)

        await self._session.commit()

        return get_converted_db_user_to_pydantic_model(result, StandartUserWithId)

    async def update_user(
            self,
            user: BaseUser,
            active: Optional[bool] = None,
            hash_password: bool = True,
            user_id: Optional[int] = None
    ) -> UserWithActive:
        """
        Replace a current database user with a user object that will passed
        and optionally change active status
        :param user_id: By this value will search in the database.
        If it is None, user_id will get from user.id(if it exist)
        :param user: The user object that will replace current user in the database
        :param active: The params that update active param in the database
        :param hash_password: This params responsible for user.password needs hash or not.
        WARNING! Disable it only when a password in the user.password already has been hashed
        if you don't want security issues or some other problems
        :return: The pydantic user object convert from a User database model
        """

        result = await usecases.update_user(
            user,
            session=self._session,
            active=active,
            hash_password=hash_password,
            user_id=user_id
        )

        await self._session.commit()

        return get_converted_db_user_to_pydantic_model(result, UserWithActive)

    async def get_user_by_id(self, user_id: int) -> UserWithActive:
        """
        It get a user from database by its id and convert this to pydantic user object
        :param user_id: By this value will search in the database
        :return: The pydantic user object convert from a User database model
        """
        result = await usecases.get_user_by_id(user_id, session=self._session)

        return get_converted_db_user_to_pydantic_model(result, UserWithActive)

    async def get_user_by_name(self, user_name: str) -> UserWithActive:
        """
        It get a user from database by his name and convert this to pydantic user object
        :param user_name: By this value will search in the database
        :return: The pydantic user object convert from a User database model
        """
        result = await usecases.get_user_by_name(user_name, session=self._session)

        return get_converted_db_user_to_pydantic_model(result, UserWithActive)

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

        result = []

        for user in users:
            result.append(
                get_converted_db_user_to_pydantic_model(user, StandartUserWithId)
            )

        return result
