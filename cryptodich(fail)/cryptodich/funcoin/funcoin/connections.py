import logging
from itertools import takewhile

logger = logging.getLogger(__name__)


class ConnectionPool:
    def __init__(self): 
        self.connection_pool = dict()

    def broadcast(self, massage):
        for user in self.connection_pool:
            user.write(f'{massage}'.encode())

    @staticmethod
    def get_address_string(writer):
        ip = writer.address['ip']
        port = writer.address['port']
        return f'{ip}:{port}'

    def add_peer(self, writer):
        address = self.get_address_string(writer)
        self.connection_pool[address] = writer
        logger.info('Added new pear to pool', address = address)

    def remove_peer(self, writer):
        address = self.get_address_string(writer)
        self.connection_pool.pop(address)
        logger.info('Removed peer from pool', address = address)


    def get_alive_peer(self, count):
        return takewhile(count, self.connection_pool.items())