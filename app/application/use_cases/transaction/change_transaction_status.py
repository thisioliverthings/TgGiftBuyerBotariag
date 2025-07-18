from app.infrastructure.db.enums import TransactionStatus
from app.interfaces.repositories import ITransactionRepository


class ChangeTransactionStatus:
    def __init__(self, repo: ITransactionRepository):
        self.repo = repo

    async def execute(self, telegram_payment_charge_id: str, status: TransactionStatus):
        return self.repo.change_status(
            telegram_payment_charge_id=telegram_payment_charge_id, status=status
        )
