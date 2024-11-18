from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import List, Optional, Union, Any, Dict

from core.middlewares.is_admin import isAdmin

class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int

def paginator(page: int = 0, count: int = 0, admin: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text=f"{page + 1} из {count}", callback_data="none"),
        InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page).pack()),
        width=3
    )
    
    if admin == "admin":
        builder.row(
            InlineKeyboardButton(text="Удалить сервер", callback_data="delete_server"),
            width=1
        )

    builder.row(
        InlineKeyboardButton(text="Добавить в избранное", callback_data="save_server_to_favorite"),
        width=1
    )
    return builder.as_markup()