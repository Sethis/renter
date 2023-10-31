

from typing import Optional, Any

from datetime import datetime

from sqlalchemy import inspect, Double, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in [*mapper.column_attrs]:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


class UnactiveToken(Base):
    __tablename__ = "unactive_tokens"
    token: Mapped[str] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    isAdmin: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[int] = mapped_column(Double(), default=0)

    def get_attributes_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "isAdmin": self.isAdmin,
            "balance": self.balance,
        }


class Transport(Base):
    __tablename__ = "transports"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    ownerId: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    canBeRented: Mapped[bool]
    transportType: Mapped[str]
    model: Mapped[str]
    color: Mapped[str]
    identifier: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(Double())
    longitude: Mapped[float] = mapped_column(Double())
    minutePrice: Mapped[Optional[float]] = mapped_column(Double(), nullable=True)
    dayPrice: Mapped[Optional[float]] = mapped_column(Double(), nullable=True)

    def get_attributes_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ownerId": self.ownerId,
            "canBeRented": self.canBeRented,
            "transportType": self.transportType,
            "model": self.model,
            "color": self.color,
            "identifier": self.identifier,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "minutePrice": self.minutePrice,
            "dayPrice": self.dayPrice
        }


class Rent(Base):
    __tablename__ = "rents"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transportId: Mapped[int] = mapped_column(BigInteger(), ForeignKey("transports.id", ondelete="CASCADE"))
    userId: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    timeStart: Mapped[datetime] = mapped_column(DateTime())
    timeEnd: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    priceOfUnit: Mapped[float]
    priceType: Mapped[str]
    finalPrice: Mapped[Optional[float]] = mapped_column(nullable=True)

    def get_attributes_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "transportId": self.transportId,
            "userId": self.userId,
            "timeStart": self.timeStart,
            "timeEnd": self.timeEnd,
            "priceOfUnit": self.priceOfUnit,
            "priceType": self.priceType,
            "finalPrice": self.finalPrice
        }
