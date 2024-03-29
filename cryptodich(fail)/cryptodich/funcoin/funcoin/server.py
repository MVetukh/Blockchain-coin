import asyncio
from asyncio import StreamReader, StreamWriter
import logging
from marshmallow.exceptions import MarshmallowError
from massages import BaseSchema
from utils import get_external_ip

logger = logging.getLogger()

class Server:
    def __init__(self, blockchain, connection_pool, p2p_protocol):
        self.blockchain = blockchain
        self.connection_pool = connection_pool
        self.p2p_protocol = p2p_protocol
        self.external_ip = None
        self.external_port = None

        if not (blockchain and connection_pool and p2p_protocol):
            logger.error("'Blockchain','connection_pool','p2p_protocol' must all be instantiated")
            raise Exception("'Could not start")

    async def get_externsl_ip(self):
        self.external_ip = await get_external_ip()
       

    async def handele_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            try: 
                data = await reader.readuntil(b'\n')
                decoded_data = data.decode('utf-8').strip()
                try:  
                    message = BaseSchema().load(decoded_data)
                except MarshmallowError:
                    logger.info('Received unreadable message', peer=writer)
                    break
                writer.address = message['meta']['address']
                self.connection_pool.add_peer(writer)
                await self.p2p_protocol.handle_message(message, writer)
                await writer.drain()
                if writer.is_closing():
                    break
            except (asyncio.exceptions.IncompleteReadError, ConnectionError):
                break
            writer.close()
            await self.connection_pool.remove_peer(writer)
    async def listen(self, hostname = '0.0.0.0', port = 8888):
        server = await asyncio.start_server(self.handele_connection, hostname, port)
        logger.info(f'listening on {hostname}:{port}')
        self.external_ip = await self.get_externsl_ip()
        self.external_port = 8888
        async with server:
            await server.serve_forever()


    
