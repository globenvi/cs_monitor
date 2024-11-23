import asyncio
import logging
import a2s
from datetime import timedelta
from core.controllers.ServerController import ServerController

# Список серверов в формате ip:port
SERVER_ADDRESSES = []

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

server_controller = ServerController()

class ServerCheckerService:
    def __init__(self, interval: int = 30):
        self.interval = interval

    async def _init_server_controller(self):
        await server_controller._init_server_controller()

    async def load_server_addresses(self):
        """Загружает IP-адреса серверов из базы данных."""
        await self._init_server_controller()
        global SERVER_ADDRESSES
        SERVER_ADDRESSES = await server_controller.get_all_server_ips()
        logging.info(f'Загруженные адреса серверов: {SERVER_ADDRESSES}')  # Отладочный вывод

    async def get_server_info(self, ip: str, port: int):
        """Функция для получения информации о сервере и игроках."""
        loop = asyncio.get_running_loop()
        address = (ip, port)
        
        try:
            server_info = a2s.info(address, timeout=10, encoding="utf-8")
            players_info = a2s.players(address, timeout=10)

            players_data = [
                {
                    'name': player.name,
                    'score': player.score,
                    'duration': str(timedelta(seconds=int(player.duration)))  # Конвертируем в часы:минуты
                }
                for player in players_info if player.duration < 86400  # Игроки, чье время меньше 24 часов
            ]
            
            return {
                'server_name': server_info.server_name,
                'map_name': server_info.map_name,
                'players': server_info.player_count,
                'max_players': server_info.max_players,
                'bots': server_info.bot_count,
                'server_type': server_info.server_type,
                'password_protected': server_info.password_protected,
                'edf': server_info.edf,
                'game': server_info.game,
                'address': f"{ip}:{port}",
                'tags': server_info.keywords,
                'vac': server_info.vac_enabled,
                'players_data': players_data
            }
        except Exception as e:
            logging.error(f'Ошибка при подключении к серверу {ip}:{port}: {e}')
            return None

    async def check_servers(self):
        await self._init_server_controller()
        await self.load_server_addresses()

        while True:
            for address in SERVER_ADDRESSES:
                ip, port_str = address.split(':')
                port = int(port_str)
                server_info = await self.get_server_info(ip, port)

                if server_info:
                    server_data = {
                        "server_name": server_info.get('server_name'),
                        "server_map": server_info.get('map_name'),
                        "players_count": server_info.get('players'),
                        "max_players": server_info.get('max_players'),
                        "game": server_info.get('game'),
                        "status": "online" if server_info.get('players') is not None else "offline",
                        "vac": server_info.get('vac'),
                        "tags": server_info.get('tags'),
                        "bots": server_info.get('bots'),
                        "server_type": server_info.get('server_type'),
                        "password_protected": server_info.get('password_protected'),
                        "edf": server_info.get('edf'),
                        "address": server_info.get('address'),
                        "players_data": server_info.get('players_data')  # Список игроков без ботов
                    }
                    await server_controller.update_server(f'{ip}:{port}', server_data)
                else:
                    logging.warning(f'Не удалось получить информацию о сервере {address}.')
                    await server_controller.update_server(f'{ip}:{port}', {"status": "offline"})

            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    checker = ServerCheckerService(interval=10)
    asyncio.run(checker.load_server_addresses())
    asyncio.run(checker.check_servers())
