from app.domain.entities import UserDTO
from app.interfaces.repositories import IUserRepository


class GetUserByTelegramId:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, telegram_id: int) -> UserDTO | None:
        return await self.repo.get_user_by_telegram_id(telegram_id=telegram_id)
