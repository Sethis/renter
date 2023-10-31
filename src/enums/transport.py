

from enum import Enum


class TransportTypes(str, Enum):
    CAR = "Car"
    BIKE = "Bike"
    SCOOTER = "Scooter"

    @classmethod
    def get_write_types(cls) -> list[str]:
        return [item for item in cls]

    @classmethod
    def get_all_types(cls) -> list[str]:
        return [item for item in cls]


# The enums cant be inherit so just repit values and plus an all-item
class TransportTypesWithAll(str, Enum):
    CAR = "Car"
    BIKE = "Bike"
    SCOOTER = "Scooter"
    ALL = "All"

    @classmethod
    def get_write_types(cls) -> list[str]:
        return [item for item in cls if item != cls.ALL]
