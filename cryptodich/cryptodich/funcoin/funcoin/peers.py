import asyncio 
import logging
from massages import create_peers_message, create_block_message, create_transaction_message,create_ping_message

logger = logging.getLogger(__name__)

class P2PError(Exception):
    pass

class P2PProtocol:
    def __init__(self, server):
        self.server = server
        self.blockchain = self.server.blockchain
        self.connection_pool = self.server.connection_pool

    @staticmethod
    async def send_message(writer, message):
        writer.write(f'{message}'.encode())


    async def handle_message(self, message, writer):
        massage_handler = {
            'block': self.handle_block,
            'ping': self.handle_ping,
            'peers': self.handle_peers,
            'transaction': self.handle_transaction,
        }
        handler = massage_handler.get(message['name'])
        if not handler:
            raise P2PError(f'Missing handler for message')
    
        await handler(message, writer)

    async def handle_ping(self, message, writer):
        block_height = message['payload']['block_height']
        writer.is_miner = message['payload']['is_miner']
        peers = self.connection_pool.get_alive_peers(20)
        peers_message = create_peers_message(self.server.external_ip, self.server.external_port, peers)
        await self.send_message(writer, peers_message)
        if block_height <self.blockchain.last_block['height']:
            for block in self.blockchain.chain[block_height+1]:
                await self.send_message(writer, create_block_message(self.server.external_ip, self.server.external_port, block))


    async def handle_transaction(self, message, writer):
        logger.info("Received transaction")
        tx = message['payload']
        if self.blockchain.validate_transaction(tx) is True:
            if tx not in self.blockchain.pending_transactions:
                self.blockchain.pending_transactions.append(tx)
                for peer in self.connection_pool.get_alive_peers(20):
                    await self.send_message(peer, create_transaction_message(self.server.external_ip, self.server.external_port, tx))
            else: logger.warning("Received invalid transaction")  


    async def handle_block(self, message, writer):
        logger.info("Received new block")
        block = message['payload']
        self.blockchain.add_block(block)

        for peer in self.connection_pool.get_alive_peers(20):
            await self.send_message(peer, create_block_message(self.server.external_ip, self.server.external_port, block))
        

    async def handle_peers(self, message, writer):
        logger.info("Received new peers")
        peers = message['payload']
        ping_message = create_peers_message(self.server.extarnal_ip,self.server.extarnal_port, len(self.self.blockchain.chain), len(self.connection_pool.get_alive_peers(50), False))
        
        for peer in peers:
            reader, writer = await asyncio.open_connection(peer['ip'], peer['port'])
            self.connection_pool.add_peer(writer)
            await self.send_message(writer, ping_message)