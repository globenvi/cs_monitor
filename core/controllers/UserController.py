import datetime
from services.DatabaseService import JSONService

class UserController:
    def __init__(self):
        self.db_service = JSONService()

    async def _init_user(self):
        await self.db_service.init()  # Инициализация базы данных

    async def create_user(self, telegram_id: int, user_data):
        """Создание пользователя с уникальным telegram_id"""
        user_data={
            "telegram_id": telegram_id,
            "username": user_data.username,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "steamid": "",
            "game_name": "",
            "role": "user",
            "last_activity": datetime.datetime.now().isoformat(),
            "profile_photo": ""
        }
        await self.db_service.create('users', user_data)

    async def get_user(self, telegram_id: int):
        """Получение данных пользователя по telegram_id"""
        return await self.db_service.find_one('users', {'telegram_id': telegram_id})

    async def update_user(self, telegram_id: int, user_data):
        """Обновление данных пользователя по telegram_id"""
        user_record = await self.get_user(telegram_id)
        if user_record:
            await self.db_service.update('users', user_record['id'], user_data)

    async def delete_user(self, telegram_id: int):
        """Удаление пользователя по telegram_id"""
        user_record = await self.get_user(telegram_id)
        if user_record:
            await self.db_service.delete('users', user_record['id'])

    async def get_all_users(self):
        """Получение всех пользователей"""
        return await self.db_service.read('users')

    async def get_users_count(self):
        """Получение количества пользователей"""
        users = await self.get_all_users()
        return len(users)

    async def update_last_activity(self, telegram_id: int):
        """Обновление времени последней активности пользователя"""
        user_record = await self.get_user(telegram_id)
        if user_record:
            user_record['last_activity'] = datetime.datetime.now().isoformat()
            await self.update_user(telegram_id, user_record)

    async def get_role(self, telegram_id: int):
        user_data = await self.db_service.find_one('users', {'telegram_id': telegram_id})
        return user_data['role'] if user_data else None
    
    async def save_server_to_favorite(self, telegram_id: int, message: str):
        server_data = message
        await self.db_service.create('favorite_servers', {'telegram_id': telegram_id, 'server': server_data})
