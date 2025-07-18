from app.core.logger import logger
from app.domain.entities import UserDTO
from app.infrastructure.db.enums import TransactionStatus, UserRole
from app.interfaces.repositories import ITransactionRepository, IUserRepository


class RefundTransaction:
    def __init__(
        self, user_repo: IUserRepository, transaction_repo: ITransactionRepository
    ):
        self.user_repo = user_repo
        self.transaction_repo = transaction_repo

    async def execute(
        self, admin_telegram_id: int, telegram_payment_charge_id: str
    ) -> dict:
        logger.info(
            f"[UseCase:RefundTransaction] Старт: admin={admin_telegram_id}, tx_id={telegram_payment_charge_id}"
        )
        admin: UserDTO = await self.user_repo.get_user_by_telegram_id(admin_telegram_id)

        if not admin or admin.role != UserRole.ADMIN:
            logger.error("[UseCase:RefundTransaction] Ошибка: not_admin")
            return {"ok": False, "error": "not_admin"}

        transaction = await self.transaction_repo.get_by_payment_charge_id(
            telegram_payment_charge_id
        )
        if not transaction:
            logger.error("[UseCase:RefundTransaction] Ошибка: transaction_not_found")
            return {"ok": False, "error": "transaction_not_found"}

        if transaction.status == TransactionStatus.REFUNDED:
            logger.error("[UseCase:RefundTransaction] Ошибка: already_refunded")
            return {"ok": False, "error": "already_refunded"}

        user: UserDTO = await self.user_repo.get_user_by_id(transaction.user_id)
        if not user:
            logger.error("[UseCase:RefundTransaction] Ошибка: user_not_found")
            return {"ok": False, "error": "user_not_found"}

        logger.info(f"[UseCase:RefundTransaction] Баланс до: {user.balance}")
        refund_amount = transaction.amount
        user = await self.user_repo.debit_user_balance(user.telegram_id, refund_amount)
        if not user:
            logger.error("[UseCase:RefundTransaction] Ошибка: debit_failed")
            return {"ok": False, "error": "debit_failed"}
        logger.info(f"[UseCase:RefundTransaction] Баланс после: {user.balance}")

        logger.info(
            f"[UseCase:RefundTransaction] Транзакция до: id={transaction.id}, status={transaction.status}"
        )
        await self.transaction_repo.change_status(
            telegram_payment_charge_id, TransactionStatus.REFUNDED
        )
        logger.info(
            f"[UseCase:RefundTransaction] Транзакция после: id={transaction.id}, status=refunded"
        )
        logger.info(
            f"[UseCase:RefundTransaction] Успех: tx_id={telegram_payment_charge_id}, amount={refund_amount}"
        )
        return {"ok": True, "refund_amount": refund_amount}
