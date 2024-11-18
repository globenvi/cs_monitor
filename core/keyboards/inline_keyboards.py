from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def get_profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить Фото", callback_data="change_photo")
            ],
            [
                InlineKeyboardButton(text="Изменить Ник", callback_data="change_nick"),
                InlineKeyboardButton(text="Изменить STEAM_ID", callback_data="change_steamid")
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=2,
    )


def admins_user_actions(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить имя", callback_data=f"update_username_id?{user_id}")
            ],
            [
                InlineKeyboardButton(text="Удалить STEAM_ID", callback_data=f"delete_steamid_id?{user_id}"),
                InlineKeyboardButton(text="Удалить фото", callback_data=f"delete_photo_id?{user_id}")
            ],
            [
                InlineKeyboardButton(text="Баны", callback_data=f"load_bans_user_id?{user_id}"),
                InlineKeyboardButton(text='Предупреждения', callback_data=f'load_warns_user_id?{user_id}')
            ],
            [
                InlineKeyboardButton(text="Комментарии админов", callback_data=f'load_admins_comments_to_user_id?{user_id}'),
                InlineKeyboardButton(text="Оставить комментарий", callback_data=f"send_admin_comment_to_user_id?{user_id}")
            ],
            [
                InlineKeyboardButton(text="Дать предупреждение", callback_data=f"send_admin_warn_to_user_id?{user_id}")
            ],
            [
                InlineKeyboardButton(text="Забанить", callback_data=f"set_ban_user_id?{user_id}"),
                InlineKeyboardButton(text="Разбанить", callback_data=f"set_unban_user_id?{user_id}"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=1,
    )