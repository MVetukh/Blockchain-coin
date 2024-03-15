import datetime
import math
import pprint
from hashlib import sha256


class Block:
    def __init__(self, prev_hash, transactor, amount):
        self.next = None
        self.__data = {
            "prev_hash": prev_hash,
            "time": datetime.datetime.now().time(),
            "transactor": transactor,
            "amount": amount,
            "hash": ""
        }
        self.__data["hash"] = self.make_hash()
    def append(self, transactor, amount):
        n = self
        while (n.next):
            n = n.next
        prev_hash = n.get_data()["hash"]
        end = Block(prev_hash, transactor, amount)
        n.next = end
    
    def get_data(self):
        return self.__data
    
    def make_hash(self):
        block_string =  (self.__data["prev_hash"] + int(int(self.__data["amount"])**1.5) + ord(self.__data["transactor"][-1]))
        return sha256(block_string).hexdigest()
    
    def set_amount(self, amount):
        self.__data["amount"] = amount
        self.__data["hash"] = self.make_hash()
        temp = self
        while (temp.next):
            prev_hash = temp.__data["hash"]
            temp = temp.next
            temp.__update_hashes(prev_hash)

    def __update_hashes(self, new_prev):
        self.__data["prev_hash"] = new_prev
        self.__data["hash"] = self.make_hash()


def print_chain(chain):
    pp = pprint.PrettyPrinter(indent=4)
    node = chain
    pp.pprint(node.get_data())
    while node.next:
        node = node.next
        pp.pprint(node.get_data())

chain = Block(0, 'Tim', 120.00)

chain.append('Jamil', 200.00)
chain.append('Carla', 123.45)
chain.append('Sarah', 450.00)

print_chain(chain)