from enum import Enum


class TransactionStatus(Enum):
    COMPLETED = "completed"
    REFUNDED = "refunded"


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"
