import os
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext

from core.controllers.UserController import UserController
from core.states.StateUserData import UserProfileForm

from core.controllers.ServerController import ServerController

router = Router()
user = UserController()
servers = ServerController()

@router.callback_query(F.data == "delete_server")
async def delete_server(callback: CallbackQuery):
    await servers._init_server_controller()
    await callback.answer('Скоро...')