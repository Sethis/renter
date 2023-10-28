

from typing import Optional

from sqlalchemy import inspect, Double, BigInteger

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self):
        mapper = inspect(self).mapper
        ent = []
        for col in [*mapper.column_attrs]:
            ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
        return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    isAdmin: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[int] = mapped_column(Double(), default=0)
    active: Mapped[bool] = mapped_column(default=False)

    def get_attributes_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "isAdmin": self.isAdmin,
            "balance": self.balance,
            "active": self.active
        }


class Transport(Base):
    __tablename__ = "transports"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ownerId: Mapped[int]
    canBeRented: Mapped[bool]
    transportType: Mapped[str]
    model: Mapped[str]
    color: Mapped[str]
    identifier: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    latitude: Mapped[int] = mapped_column(Double())
    longitude: Mapped[int] = mapped_column(Double())
    minutePrice: Mapped[Optional[int]] = mapped_column(Double(), nullable=True)
    dayPrice: Mapped[Optional[int]] = mapped_column(Double(), nullable=True)
