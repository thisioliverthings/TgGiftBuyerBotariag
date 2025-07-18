from abc import ABC, abstractmethod

from app.domain.entities import TransactionDTO
from app.infrastructure.db.enums import TransactionStatus


class ITransactionRepository(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: int,
        amount: int,
        telegram_payment_charge_id: str,
        status: TransactionStatus,
        payload: str,
    ) -> TransactionDTO | None: ...

    @abstractmethod
    async def change_status(
        self, telegram_payment_charge_id: str, status: TransactionStatus
    ) -> TransactionDTO | None: ...

    @abstractmethod
    async def get_by_payment_charge_id(
        self, telegram_payment_charge_id: str
    ) -> TransactionDTO | None: ...

    @abstractmethod
    async def get_last_user_transactions(
        self, user_id: int, limit: int = 5
    ) -> list[TransactionDTO]: ...

    @abstractmethod
    async def get_user_transactions_paginated(
        self, user_id: int, offset: int, limit: int
    ) -> list[TransactionDTO]: ...

    @abstractmethod
    async def get_user_transactions_count(self, user_id: int) -> int: ...
