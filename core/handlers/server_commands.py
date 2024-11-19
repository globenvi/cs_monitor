import os
import asyncio
from aiogram import Router, Bot, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

from core.controllers.UserController import UserController
from core.controllers.CommandController import CommandController
from core.controllers.ServerController import ServerController
from services.ServerCheckerService import ServerCheckerService
from core.keyboards.inline_pagination import Pagination, paginator

router = Router()
user = UserController()
commands = CommandController()
server_controller = ServerController()
load_checker = ServerCheckerService()

items_per_page = 5  # Количество серверов на странице

@router.callback_query(Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: Pagination):
    await server_controller._init_server_controller()
    await load_checker.load_server_addresses()
    servers = await server_controller.get_all_servers_list()

    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(servers) - 1) else page_num

    # Обновляем серверы для текущей страницы
    map_name = servers[page][4]
    file_path = f'core/data/images/maps/{map_name}.jpeg'
    default_path = 'core/data/images/maps/def_image.jpeg'

    # Проверяем, существует ли файл для карты
    photo = FSInputFile(file_path) if os.path.isfile(file_path) else FSInputFile(default_path)

    # Формируем информацию о сервере
    server_info = (
        f"<b>{servers[page][3]}</b>\n"                      # Название сервера
        f"🗺️ {servers[page][4]} | "                         # Карта
        f"👥 {servers[page][5]} | "                         # Количество игроков
        f"📶 {servers[page][2]}\n\n"                        # Статус сервера
        f"🎮 {servers[page][7]}\n\n"                        # Игра
        f"📍<i>{servers[page][9]}</i>\n\n"                  # Теги сервера
        f"🌐 IP: <code>{servers[page][1]}</code>\n\n"       # IP:PORT
        f"🔗 Подключение:\n<pre>connect {servers[page][1]}</pre>\n\n"  # Команда подключения
    )

    # Добавляем информацию об игроках, если есть
    players_data = servers[page][-1]  # Список игроков
    if players_data:
        for player in players_data:
            server_info += f"🟢 {player['name']} | {player['score']}\n"

    with suppress(TelegramBadRequest):
        await call.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=server_info),
            reply_markup=paginator(page, len(servers))
        )

        await call.message.edit_caption(
            caption=server_info,
            reply_markup=paginator(page, len(servers)),
            parse_mode='html'
        )
        await call.answer()

@router.message(Command('servers'))
async def get_servers(message: Message):
    await server_controller._init_server_controller()
    await load_checker.load_server_addresses()

    # Получаем все сервера из контроллера
    servers = await server_controller.get_all_servers_list()

    map_name = servers[0][4]
    file_path = f'core/data/images/maps/{map_name}.jpeg'
    default_path = 'core/data/images/maps/def_image.jpeg'

    # Проверяем, существует ли файл для карты
    photo = FSInputFile(file_path) if os.path.isfile(file_path) else FSInputFile(default_path)

    # Формируем информацию о первом сервере
    server_info = (
        f"<b>{servers[0][3]}</b>\n"  # Название сервера
        f"🗺️ {servers[0][4]} | "  # Карта
        f"👥 {servers[0][5]} | "  # Количество игроков
        f"📶 {servers[0][2]}\n\n"
        f"🎮 {servers[0][7]}\n\n"
        f"📍<i>{servers[0][9]}</i>\n\n"
        f"🌐 IP: <code>{servers[0][1]}</code>\n\n"  # IP:PORT
        f"🔗 Подключение:\n<pre>connect {servers[0][1]}</pre>\n\n"
    )

    # Добавляем информацию об игроках, если есть
    players_data = servers[0][-1]  # Список игроков
    if players_data:
        for player in players_data:
            server_info += f"🟢 {player['name']} | {player['score']}\n"

    await message.answer_photo(
        photo=photo,
        caption=server_info,
        reply_markup=paginator(0, len(servers), await user.get_role(message.from_user.id)),
        parse_mode='html'
    )

@router.message(F.text == "🌐 Сервера")
async def back_to_profile(message: Message):
    await user._init_user()
    await get_servers(message)
    await user.update_last_activity(message.from_user.id)
