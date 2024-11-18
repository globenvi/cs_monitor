import os, asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from core.controllers.UserController import UserController
from core.controllers.CommandController import CommandController

from core.keyboards.reply_keyboards import main_keyboard
from core.keyboards.inline_keyboards import get_profile_keyboard

from core.middlewares.is_admin import isAdmin

router = Router()
user = UserController()
commands = CommandController()


async def register_commands():
    await commands._init_commands()

    await commands.add_command('start', 'Запустить бота')
    await commands.add_command('profile', 'Просмотреть свой профиль')
    await commands.add_command('help', 'Посмотреть список команд')
    await commands.add_command('servers', 'Список серверов')


@router.message(Command('start'))
async def startUp(message: Message):
    await register_commands()
    await user._init_user()

    if await user.get_users_count() == 0:
        await user.create_user(message.from_user.id, message.from_user)
        await user.update_user(message.from_user.id, {'role': 'admin'})
        await user.update_last_activity(message.from_user.id)
        await message.reply(f"Привет, <b>{message.from_user.first_name}</b>!\nЧто бы посмотреть список доступных команд используй /help", parse_mode='html', reply_markup=main_keyboard)
    else:
        if not await user.get_user(message.from_user.id):
            await user.create_user(message.from_user.id, message.from_user)
            await user.update_last_activity(message.from_user.id)
            await message.reply(f"Привет, <b>{message.from_user.first_name}</b>!\nЧто бы посмотреть список доступных команд используй /help", parse_mode='html', reply_markup=main_keyboard)
        else:
            await user.update_last_activity(message.from_user.id)
            await message.reply(f"C возвращением <b>{message.from_user.first_name}</b>!\n", parse_mode='html', reply_markup=main_keyboard)


@router.message(Command('profile'))
async def profile(message: Message, user_id: int = None):
    if message.chat.type == 'private':
        await user._init_user()  # Инициализация пользователя


        # Получение данных пользователя
        user_data = await user.get_user(message.from_user.id)

        if message.from_user:
            user_data = await user.get_user(message.from_user.id)

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
                    await message.answer_photo(photo, caption=profile_info, parse_mode='HTML', reply_markup=get_profile_keyboard())
                else:
                    await message.answer( profile_info, parse_mode='HTML', reply_markup=get_profile_keyboard())

        if user_id:
            user_data = await user.get_user(user_id)

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
                    await message.answer_photo(photo, caption=profile_info, parse_mode='HTML', reply_markup=get_profile_keyboard())
                else:
                    await message.answer( profile_info, parse_mode='HTML', reply_markup=get_profile_keyboard())


        if user_data is None:
            await message.answer("Профиль не найден. Используйте /start, чтобы зарегистрироваться.")
    else:
        await message.answer("Частаная информация, не стоит запрашивать ее в группе! ;)")


@router.message(Command('help'))
async def help(message: Message):
    await commands._init_commands()  # Инициализация команд
    command_list = await commands.get_command_list()
    await message.reply(f"Список доступных команд:\n\n{command_list}")

# !ТЕКСТОВЫЕ ТРИГЕРЫ
# ?ВНИМАНИЕ Обычные сообщения перехватывать в самом низу!
@router.message(F.text == "😎 Профиль")
async def back_to_profile(message: Message):
    await user._init_user()
    await profile(message)
    await user.update_last_activity(message.from_user.id)