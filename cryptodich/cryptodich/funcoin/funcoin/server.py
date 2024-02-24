import asyncio
from asyncio import StreamReader, StreamWriter
import logging
from marshmallow.exceptions import MarshmallowError
from funcoin.massages import BaseSchema
from funcoin.utils import get_external_ip

logger = logging.getLogger()

class Server:
    def __init__(self, blockchain, connection_pool, p2p_protocol):
        pass

    async def get_externsl_ip(self):
        pass

    async def handele_connection(self, render: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            try: pass
            except (asyncio.exceptions.IncompleteReadError, ConnectionError):pass
    async def listen(self, hostname = '0.0.0.0', port = 8888):
        server = await asyncio.start_server(self.handele_connection, hostname, port)
        asyncio.logger.info(f'listening on {hostname}:{port}')
        async with server:
            await server.serve_forever()


    
