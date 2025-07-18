from sqlalchemy import desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.domain.entities import TransactionDTO
from app.infrastructure.db.enums import TransactionStatus
from app.infrastructure.db.models import TransactionModel
from app.interfaces.repositories import ITransactionRepository


class TransactionRepository(ITransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        amount: int,
        telegram_payment_charge_id: str,
        status: TransactionStatus,
        payload: str,
    ) -> TransactionDTO | None:
        existing_transaction = await self.session.scalar(
            select(TransactionModel).where(
                TransactionModel.telegram_payment_charge_id
                == telegram_payment_charge_id
            )
        )
        if existing_transaction:
            return None

        transaction = TransactionModel(
            user_id=user_id,
            amount=amount,
            telegram_payment_charge_id=telegram_payment_charge_id,
            status=status,
            payload=payload,
        )
        self.session.add(transaction)
        await self.session.flush()

        logger.info(
            f"[TransactionRepo] Создана транзакция: id={transaction.id}, user_id={user_id}, amount={amount}, status={status}"
        )

        return TransactionDTO(
            id=transaction.id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            telegram_payment_charge_id=transaction.telegram_payment_charge_id,
            status=transaction.status,
            payload=transaction.payload,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )

    async def change_status(
        self, telegram_payment_charge_id: str, status: TransactionStatus
    ) -> TransactionDTO | None:
        existing_transaction = await self.session.scalar(
            select(TransactionModel).where(
                TransactionModel.telegram_payment_charge_id
                == telegram_payment_charge_id
            )
        )

        if not existing_transaction:
            return None

        existing_transaction.status = status

        logger.info(
            f"[TransactionRepo] Изменён статус транзакции: id={existing_transaction.id}, user_id={existing_transaction.user_id}, status={status}"
        )

        return TransactionDTO(
            id=existing_transaction.id,
            user_id=existing_transaction.user_id,
            amount=existing_transaction.amount,
            telegram_payment_charge_id=existing_transaction.telegram_payment_charge_id,
            status=existing_transaction.status,
            payload=existing_transaction.payload,
            created_at=existing_transaction.created_at,
            updated_at=existing_transaction.updated_at,
        )

    async def get_by_payment_charge_id(
        self, telegram_payment_charge_id: str
    ) -> TransactionDTO | None:
        transaction = await self.session.scalar(
            select(TransactionModel).where(
                TransactionModel.telegram_payment_charge_id
                == telegram_payment_charge_id
            )
        )

        if not transaction:
            return None

        return TransactionDTO(
            id=transaction.id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            telegram_payment_charge_id=transaction.telegram_payment_charge_id,
            status=transaction.status,
            payload=transaction.payload,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )

    async def get_last_user_transactions(
        self, user_id: int, limit: int = 5
    ) -> list[TransactionDTO]:
        result = await self.session.execute(
            select(TransactionModel)
            .where(TransactionModel.user_id == user_id)
            .order_by(desc(TransactionModel.created_at))
            .limit(limit)
        )
        transactions = result.scalars().all()
        return [
            TransactionDTO(
                id=tx.id,
                user_id=tx.user_id,
                amount=tx.amount,
                telegram_payment_charge_id=tx.telegram_payment_charge_id,
                status=tx.status,
                payload=tx.payload,
                created_at=tx.created_at,
                updated_at=tx.updated_at,
            )
            for tx in transactions
        ]

    async def get_user_transactions_paginated(
        self, user_id: int, offset: int, limit: int
    ) -> list[TransactionDTO]:
        result = await self.session.scalars(
            select(TransactionModel)
            .where(TransactionModel.user_id == user_id)
            .order_by(desc(TransactionModel.created_at))
            .offset(offset)
            .limit(limit)
        )
        transactions = result.all()
        return [
            TransactionDTO(
                id=tx.id,
                user_id=tx.user_id,
                amount=tx.amount,
                telegram_payment_charge_id=tx.telegram_payment_charge_id,
                status=tx.status,
                payload=tx.payload,
                created_at=tx.created_at,
                updated_at=tx.updated_at,
            )
            for tx in transactions
        ]

    async def get_user_transactions_count(self, user_id: int) -> int:
        result = await self.session.scalar(
            select(func.count(TransactionModel.id)).where(
                TransactionModel.user_id == user_id
            )
        )
        return result if result else 0
