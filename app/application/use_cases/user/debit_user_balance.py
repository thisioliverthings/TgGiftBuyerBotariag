from app.domain.entities import UserDTO
from app.interfaces.repositories import IUserRepository


class DebitUserBalance:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, telegram_id: int, amount: int) -> UserDTO:
        return await self.repo.debit_user_balance(
            telegram_id=telegram_id, amount=amount
        )
