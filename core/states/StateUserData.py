from aiogram.fsm.state import State, StatesGroup

class UserProfileForm(StatesGroup):
    name = State()
    age = State()
    game_name = State()
    steamid = State()
    about = State()
    bio = State()
    photo = State()
    confirm = State()
    