from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema
from funcoin.schema import Peer, Block, Transaction, Ping

class PeersMessage(Schema):
    payload = fields.Nested(Peer(many = True))

    @post_load
    def add_name(self, data, **kwargs):
        data['name'] = 'peers'
        return data

class BlockMessage(Schema):
    payload = fields.Nested(Block)
    
    @post_load
    def add_name(self, data, **kwargs):
        data['name'] = 'blocks'
        return data

class TransactionMessage(Schema):
    payload = fields.Nested(Transaction)

class PingMessage(Schema):
    payload = fields.Nested(Ping)

    @post_load
    def add_name(self, data, **kwargs):
        data['name'] = 'ping'
        return data
    
class MessageDisabiguation(OneOfSchema):
    type_field = 'name'
    type_schemas = {
        'peers': PeersMessage,
        'blocks': BlockMessage,
        'ping': PingMessage,
        'transactions': TransactionMessage
    }

    def get_obj_type(self, obj):
        if isinstance(obj, dict):
            return obj.get('name')
        
class MetaSchema(Schema):
    address = fields.Nested(Peer())
    client = fields.Str()

class BaseSchema(Schema):
    meta = fields.Nested(MetaSchema())
    message = fields.Nested(MessageDisabiguation())

    def meta(self,ip, port, version = '0.1'):
        return {
            'client': version,
            'address': {
                'ip': ip,
                'port': port
            }
        }
    
    def create_peers_message(self,external_ip, external_port, peers):
        return BaseSchema().dumps(
            {
                'meta': self.meta(external_ip, external_port),
                'message':{
                    'name': 'peers',
                    'payload': peers
                }
            }
        )

    def create_transactions_message(self,external_ip, external_port,tx):
        return BaseSchema().dumps(
            {
                "meta": self.meta(external_ip, external_port),
                 "message": {
                 "name": "transaction",
                 "payload": tx,
                 }
            }
            )

    