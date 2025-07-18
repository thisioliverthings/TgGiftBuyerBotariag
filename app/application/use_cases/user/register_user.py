from app.domain.entities import UserDTO
from app.interfaces.repositories import IUserRepository


class RegisterUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, telegram_id: int, username: str) -> UserDTO:
        existing_user = await self.repo.get_by_telegram_id(telegram_id)

        if existing_user:
            return existing_user

        return await self.repo.create(telegram_id=telegram_id, username=username)
