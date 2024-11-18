import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext

from core.controllers.UserController import UserController
from core.states.StateUserData import UserProfileForm

router = Router()
user = UserController()

@router.callback_query(F.data == 'change_photo')
async def change_photo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserProfileForm.photo)
    await callback.message.answer("Отправьте фотографию.")

@router.message(UserProfileForm.photo)
async def get_photo(message: Message, state: FSMContext):
    await user._init_user()
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(photo=file_id)
        await user.update_user(message.from_user.id, {'profile_photo': file_id})
        await state.clear()
        await message.answer("Фотография успешно обновлена. Загляни в /profile")
    else:
        await message.answer("Пожалуйста, отправьте фотографию.")
        await user.update_last_activity(message.from_user.id)


@router.callback_query(F.data == 'change_nick')
async def change_nick(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserProfileForm.name)
    await callback.message.answer("Введите новый никнейм.")

@router.message(UserProfileForm.name)
async def get_nick(message: Message, state: FSMContext):
    await user._init_user()
    await user.update_user(message.from_user.id, {'game_name': message.text})
    await state.clear()
    await message.answer("Никнейм успешно обновлен. Загляни в /profile")
    await user.update_last_activity(message.from_user.id)


@router.callback_query(F.data == 'change_steamid')
async def change_steamid(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserProfileForm.steamid)
    await callback.message.answer("Введите новый steamid.")
    await callback.message.answer("<b>!!!ЧИТАЙТЕ ВНИМАНТЕЛЬНО!!!</b>\n\n <blockquote>Если вы укажите не верный STEAM_ID, то не сможете взаимодействовать с сервером.\nНе будет работать ни статистика, ни какие либо другие функции!\nПРОПИСАТЬ ID можно только 1 раз!</blockquote>", parse_mode="HTML")

@router.message(UserProfileForm.steamid)
async def get_steamid(message: Message, state: FSMContext):
    await user._init_user()
    if user.get_user(message.from_user.id)['steam_id'] is None:
        if "STEAM_:" in message.text and len(message.text) > 15:
            await user.update_user(message.from_user.id, {'steamid': message.text})
            await state.clear()
            await message.answer("Steamid успешно обновлен. Загляни в /profile")
        else:
            await message.answer("Пожалуйста, введите корректный steamid. Пример - STEAM_:763218767376187")
            await user.update_last_activity(message.from_user.id)

    else:
        await message.answer("У вас уже установлен STEAM_ID! Если вы ошиблись в написании, свяжитесь с администратором!")

@router.callback_query(F.data == 'save_server_to_favorite')
async def save_server_to_favorite(callback: CallbackQuery):
    await user._init_user()
    await user.save_server_to_favorite(callback.from_user.id, callback.message.text)
    await callback.answer("Сервер добавлен в избранное!")