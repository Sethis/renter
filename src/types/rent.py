

from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from src.enums.rent import PriceTypes


class RentType(BaseModel):
    rentType: PriceTypes


class RentId(BaseModel):
    id: int


class StandartRent(BaseModel):
    transportId: int
    userId: int
    timeStart: datetime
    timeEnd: Optional[datetime] = None
    priceOfUnit: float
    priceType: PriceTypes
    finalPrice: Optional[float] = None


class FullRent(RentId, StandartRent):
    pass

