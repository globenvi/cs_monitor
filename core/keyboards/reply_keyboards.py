from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="😎 Профиль")
        ],
        [
            KeyboardButton(text="🌐 Сервера"),
            # KeyboardButton(text='💊 Тех.Поддержка')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    row_width=2,
    selective=True,  # optional, defaults to False
)