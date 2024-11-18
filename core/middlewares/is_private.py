# core/middlewares/is_private.py
from aiogram import BaseMiddleware
from aiogram.types import Message

class isPrivate(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        # Проверяем, если чат приватный
        if event.chat.type != "private":
            await event.answer("Эта команда доступна только в приватных чатах.")
            return  # Прерываем выполнение команды
        return await handler(event, data)
