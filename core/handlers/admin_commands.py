import os, asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from core.controllers.UserController import UserController
from core.controllers.CommandController import CommandController
from core.controllers.ServerController import ServerController

from core.keyboards.reply_keyboards import main_keyboard
from core.keyboards.inline_keyboards import admins_user_actions

from core.middlewares.is_admin import isAdmin

from services.ServerCheckerService import ServerCheckerService

router = Router()
user = UserController()
server = ServerController()
server_service = ServerCheckerService()


@router.message(Command('check'), isAdmin())
async def check_user(message: Message, bot: Bot):
    await user._init_user()
    
    if message.reply_to_message.from_user.id != message.from_user.id:
        user_data = await user.get_user(message.reply_to_message.from_user.id)

        if user_data:
            # Формирование сообщения о профиле
            profile_info = (
                f"<b>ID</b>: {user_data['telegram_id']}\n"
                f"<b>Username</b>: {user_data.get('username', 'Не указано')}\n"
                f"<b>Ник в игре</b>: {user_data.get('game_name', 'Не указано')}\n"
                f"<b>SteamID</b>: {user_data.get('steamid', 'Не указано')}\n\n"
            )

            if user_data.get('profile_photo'):
                photo = user_data.get('profile_photo')
                await bot.send_photo(message.from_user.id, photo, caption=profile_info, parse_mode='HTML', reply_markup=admins_user_actions(message.reply_to_message.from_user.id))
            else:
                await bot.send_message(message.from_user.id, profile_info, parse_mode='HTML', reply_markup=admins_user_actions(message.reply_to_message.from_user.id))

@router.message(Command('add_server'), isAdmin())
async def add_server(message: Message,):
    await server._init_server_controller()
    await server.add_server(message.from_user.id, message.text.split()[1])
    await message.reply("Сервер добавлен!")
    await server_service.load_server_addresses()