from services.DatabaseService import JSONService


class ServerController(JSONService):
    def __init__(self,):
        self.db_service = JSONService()


    async def _init_server_controller(self):
        await self.db_service.init()

    async def add_server(self, telegram_id: int, serverIP: str):
        server_data = {
            "owner": telegram_id,
            "ip": serverIP,
            "status": "cheking",
            "server_name": None,
            "server_map": None,
            "players_count": None,
            "max_players": None,
            'game': None,
            'vac': None,
            'tags': None,
            'bots': None,
            'server_type': None,
            'version': None,
            'password_protected': None,
            'edf': None,
            'address': None
            }
        await self.db_service.create('servers', server_data)
    
    async def get_server(self, serverIP: str):
        return await self.db_service.find_one('servers', {'ip': serverIP})
    
    async def get_servers(self):
        return await self.db_service.read('servers')
    
    async def update_server(self, serverIP: str, server_data):
        server_record = await self.get_server(serverIP)
        if server_record:
            await self.db_service.update('servers', server_record['id'], server_data)
            

    async def get_all_server_ips(self):
        """Получает все IP-адреса серверов из базы данных."""
        servers = await self.get_servers()
        return [server['ip'] for server in servers if 'ip' in server]
    
    async def get_all_servers_list(self):
        """Получает информацию о всех серверах в виде списков."""
        servers = await self.get_servers()
        return [
            [
                server.get('owner'),          # Owner of the server
                server.get('ip'),             # IP address of the server
                server.get('status'),         # Status of the server
                server.get('server_name'),    # Server name
                server.get('server_map'),     # Current map of the server
                server.get('players_count'),    # Current number of players on the server
                server.get('max_players'),    # Maximum number of players allowed on the server
                server.get('game'),           # Game being played on the server
                server.get('vac'),            # VAC status of the server
                server.get('tags'),           # Tags associated with the server
                server.get('bots'),           # Number of bots on the server
                server.get('server_type'),    # Type of the server
                server.get('version'),        # Version of the server
                server.get('password_protected'),  # Whether the server is password-protected
                server.get('edf'),            # EDF status of the server
                server.get('address'),        # Address of the server
                server.get('players_data')    # Players info
            ]
            for server in servers
        ]

    async def get_servers_by_filter(self, filter_dict):
        """Получает список серверов по заданному фильтру."""
        return await self.db_service.find('servers', filter_dict)