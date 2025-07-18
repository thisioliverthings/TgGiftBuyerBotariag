from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from . import UserModel


class AutoBuySettingModel(Base):
    __tablename__ = "auto_buy_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, index=True, nullable=False
    )

    status: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    price_limit_from: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    price_limit_to: Mapped[int] = mapped_column(Integer, default=10**9, nullable=False)

    supply_limit: Mapped[int] = mapped_column(Integer, default=10**9)

    cycles: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="auto_buy_setting")
