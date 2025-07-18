from dataclasses import dataclass

from app.infrastructure.db.enums import UserRole


@dataclass(frozen=True)
class UserDTO:
    id: int
    telegram_id: int
    username: str
    balance: int
    role: UserRole
    notifications_enabled: bool
    language: str
