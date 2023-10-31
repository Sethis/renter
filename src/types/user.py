

from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    password: str

    def get_balance(self) -> int:
        return self.__dict__.get("balance", 0)

    def get_balance_is_exists(self) -> bool:
        return self.__dict__.get("balance", None) is not None

    def get_admin_status(self) -> bool:
        return self.__dict__.get("isAdmin", False)

    def get_admin_status_is_exists(self) -> bool:
        return self.__dict__.get("isAdmin", None) is not None

    def get_id(self) -> Optional[int]:
        return self.__dict__.get("id", None)

    def get_id_is_exists(self) -> bool:
        return self.get_id() is not None


class PlainUser(BaseUser):
    pass


class StandartUser(BaseUser):
    isAdmin: bool
    balance: int


class StandartUserWithId(StandartUser):
    id: int
