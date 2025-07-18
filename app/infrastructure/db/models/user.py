from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..enums import UserRole

if TYPE_CHECKING:
    from .auto_buy_setting import AutoBuySettingModel
    from .transaction import TransactionModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True, index=True
    )

    username: Mapped[str] = mapped_column(String, nullable=False)

    balance: Mapped[int] = mapped_column(Integer, default=0)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.USER, nullable=False
    )

    notifications_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)

    language: Mapped[str] = mapped_column(String, default="ru", nullable=False)

    auto_buy_setting: Mapped["AutoBuySettingModel"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )

    transactions: Mapped[list["TransactionModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
