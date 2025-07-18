from dataclasses import dataclass
from datetime import datetime

from app.infrastructure.db.enums import TransactionStatus


@dataclass(frozen=True)
class TransactionDTO:
    id: int
    user_id: int
    amount: int
    telegram_payment_charge_id: str
    payload: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
