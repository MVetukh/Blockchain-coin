from datetime import datetime
from hashlib import sha256
import json
import random
from time import time
import logging
import asyncio
import math

logger = logging.getLogger("blockchain")

class Blockchain():
    def __init__(self) -> dict:
        self.chain: list = []
        self.pending_transactions: list= []
        self.target = "0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        logger.info('creating blockchain of down from class corection')
        self.new_block()
    def new_block(self) -> dict:
      block = self.create_block(
          height = len(self.chain),
          # 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          transactions = self.pending_transactions,
          
          previous_hash = self.last_block()['hash'] if self.last_block() else None, # Исправлено на вызов метода
          nonce = format(random.getrandbits(64), "x"),
          target = self.target,
          timestamp = time())
      #block_hash: str = self.hash(block)
      #block['hash'] = block_hash
      self.pending_transactions = []
      # self.chain.append(block)
      # print (f"Created block {block['index']}")
            
      return block

    
    @staticmethod
    def create_block(height: int, transactions: list, previous_hash: str, nonce: str, target: str, timestamp: str = None) -> dict:
        block = {
            'index': height ,
            'transactions': transactions,
            'previous_hash': previous_hash,
            'nonce': nonce,
            'target': target,
            'timestamp': timestamp or time()
        }
        block_string = json.dumps(block, sort_keys=True).encode()
        block['hash'] = sha256(block_string).hexdigest()
        return block
    
    @staticmethod
    def hash(block) -> str:
        block_string: str = json.dumps(block, sort_keys=True, indent=52, default=str).encode()
        return sha256(block_string).hexdigest()

    def last_block(self) -> list:
        return self.chain[-1] if self.chain else None

    def valid_block(self, block):
        return block['hash'] < self.target

    def add_block(self, block):
        self.chain.append(block)

    def recalculate_target(self, block_index):
       
        # Проверяем, нужно ли нам пересчитывать заданное
        if block_index % 10 == 0:
        # Ожидаемый промежуток времени 10 блоков
            expected_timespan = 10 * 10
            # Рассчитываем фактический промежуток времени
            actual_timespan = self.chain[-1]["timestamp"] 
            self.chain[-10]["timestamp"]
            # Выясняем смещение
            ratio = actual_timespan / expected_timespan
            # Теперь давайте настроим соотношение так, чтобы оно
            #не было слишком экстремальным
            ratio = max(0.25, ratio)
            ratio = min(4.00, ratio)
            # Рассчитайте новое заданное значение, умножив
            new_target = int(self.target, 16) * ratio
            self.target = format(math.floor(new_target),"x").zfill(64)
            logger.info(f"Calculated new mining target:{self. target}")
        return self.target
    
    def new_transaction(self, sender,recipient, amount):
        self.pending_transactions.append(
            {
                'recipient':recipient,
                'sender':sender,
                'amount':amount
            }
        )
    
    async def get_blocks_after_timestamp(self, timestamp):
        for index,  block in enumerate(self.chain):
            if block['timestamp'] > timestamp:
                return self.chain[index:]
    
    async def mine_new_blocks(self):
        self.recalculate_target(self.last_block['index']+1)
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                break
                await asyncio.sleep(0)

        self.chain.append(new_block)
        print('Found new block', new_block)

    # def proof_of_work(self):
    #     while True:
    #         new_block = self.new_block()
    #         if self.valid_hash(new_block):
    #             break
        
    #     self.chain.append(new_block)
    #     print('Found new block', new_block)

    # @staticmethod
    # def valid_hash(block):# -> Any:
    #     return block['hash'].startswith('0000')

if __name__ == '__main__':
    bc = Blockchain()
    info: dict = bc.create_block
    print(info)
