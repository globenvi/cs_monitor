from aiogram.filters import BaseFilter
from aiogram.types import Message
from core.controllers.UserController import UserController


class isAdmin(BaseFilter):
    def __init__(self):
        self.user_controller = UserController()
        self.admin_ids = []

    async def load_admins(self):
        """Загружает всех пользователей с ролью admin и сохраняет их telegram_id в admin_ids"""
        await self.user_controller._init_user()
        users = await self.user_controller.db_service.find_all('users', {'role': 'admin'})
        self.admin_ids = [user['telegram_id'] for user in users]

    async def __call__(self, message: Message) -> bool:
        if not self.admin_ids:
            await self.load_admins()
        return message.from_user.id in self.admin_ids
