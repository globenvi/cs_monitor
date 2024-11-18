from services.DatabaseService import JSONService



class CommandController(JSONService):
    
    def __init__(self):
        self.db_service = JSONService()

    async def _init_commands(self):
        await self.db_service.init()  # Инициализация базы данных


    async def add_command(self, command: str, description: str):
        command_data = {
            "command": command,
            "description": description
        }
        await self.db_service.create('commands', command_data)

    async def get_command(self, command: str):
        return await self.db_service.find_one('commands', {'command': command})
    
    async def get_commands(self):
        return await self.db_service.read('commands')
    
    async def delete_command(self, command: str):
        command_record = await self.get_command(command)
        if command_record:
            await self.db_service.delete('commands', command_record['id'])

    async def update_command_description(self, command: str, new_description: str):
        command_record = await self.get_command(command)
        if command_record:
            command_record['description'] = new_description
            await self.db_service.update('commands', command_record['id'], command_record)

    async def get_command_list(self):
        commands = await self.get_commands()
        command_list = []
        for command in commands:
            command_text = f"/{command['command']} - {command.get('description', 'Описание не доступно')}"
            command_list.append(command_text)
        return "\n".join(command_list)  # Объединяем список в строку с переносами
