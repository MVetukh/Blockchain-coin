from datetime import datetime
from hashlib import sha256
import json
import random

class Blockchain():
    def __init__(self) -> dict:
        self.chain: list = []
        self.pending_transactions: list= []

        print('creating blockchain of down from class corection')
        self.new_block()
    def new_block(self) -> dict:
        block: dict = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'transactions': self.pending_transactions,
            #'proof': self.proof_of_work(previous_hash),
            'previous_hash': self.last_block() if self.last_block else None,
            'nonce': format(random.getrandbits(64), "x"),
        }
        block_hash: str = self.hash(block)
        block['hash'] = block_hash

        # self.pending_transactions = []
        # self.chain.append(block)
        # print (f"Created block {block['index']}")
              
        return block

    @staticmethod
    def hash(block) -> str:
        block_string: str = json.dumps(block, sort_keys=True, indent=4, default=str).encode()
        return sha256(block_string).hexdigest()

    def last_block(self) -> list:
        return self.chain[-1] if self.chain else None

    def new_transaction(self, sender,recipient, amount):
        self.pending_transactions.append(
            {
                'recipient':recipient,
                'sender':sender,
                'amount':amount
            }
        )
    
    def proof_of_work(self):
        while True:
            new_block = self.new_block()
            if self.valid_hash(new_block):
                break
        
        self.chain.append(new_block)
        print('Found new block', new_block)

    @staticmethod
    def valid_hash(block):# -> Any:
        return block['hash'].startswith('0000')

if __name__ == '__main__':
    bc = Blockchain()
    info: dict = bc.proof_of_work()
    print(info)
