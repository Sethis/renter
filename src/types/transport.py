

from typing import Optional

from pydantic import BaseModel

from src.enums.transport import TransportTypes


class BaseTransport(BaseModel):
    canBeRented: bool
    model: str
    color: str
    identifier: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    minutePrice: Optional[float] = None
    dayPrice: Optional[float] = None

    def get_owner_id(self) -> Optional[int]:
        return self.__dict__.get("ownerId", None)

    def get_owner_id_is_exist(self) -> bool:
        return self.get_owner_id() is not None

    def get_transport_id(self) -> Optional[int]:
        return self.__dict__.get("id", None)

    def get_transport_id_is_exist(self) -> bool:
        return self.get_transport_id() is not None

    def get_transport_type(self) -> Optional[int]:
        return self.__dict__.get("transportType", None)

    def get_transport_type_is_exist(self) -> bool:
        return self.get_transport_type() is not None


class TransportWithOwner(BaseModel):
    ownerId: int


class TransportWithId(BaseModel):
    id: int


class TransportWithType(BaseModel):
    transportType: TransportTypes


class UserWriteTransport(BaseTransport, TransportWithType):
    pass


class WriteTransport(BaseTransport, TransportWithOwner, TransportWithType):
    pass


class EditTransport(BaseTransport):
    pass


class FullTransport(BaseTransport, TransportWithId, TransportWithOwner, TransportWithType):
    pass
