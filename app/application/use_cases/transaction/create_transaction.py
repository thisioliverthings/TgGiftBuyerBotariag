from app.domain.entities import TransactionDTO
from app.infrastructure.db.enums import TransactionStatus
from app.interfaces.repositories import ITransactionRepository


class CreateTransaction:
    def __init__(self, repo: ITransactionRepository):
        self.repo = repo

    async def execute(
        self,
        user_id: int,
        amount: int,
        telegram_payment_charge_id: str,
        status: TransactionStatus,
        payload: str,
    ) -> TransactionDTO | None:
        return await self.repo.create(
            user_id=user_id,
            amount=amount,
            telegram_payment_charge_id=telegram_payment_charge_id,
            status=status,
            payload=payload,
        )
