import json
from time import time
from marshmallow import Schema, fields, validates_schema, ValidationError


class Transaction(Schema):
    timestamp = fields.Int()
    sender = fields.Str()
    receiver = fields.Str()
    amount = fields.Int()
    signature = fields.Str()

    class Meta:
        ordered = True

class Block(Schema):
    mined_by = fields.Str(required=False)
    transactions = fields.Nested(Transaction(), many = True)
    height = fields.Int(required=True)
    target = fields.Str(required=True)
    hash = fields.Str(required=True)
    previous_hash = fields.Str(required=True)
    nonce = fields.Str(required=True)
    timestamp = fields.Str(required=True)

    class Meta:
        ordered = True

    @validates_schema
    def validate_block(self, data, **kwargs):
        block = data.copy()
        block.pop('hash')
    
        if data['hash'] != json.dumps(block, keys=True):
            raise ValidationError('Fraudulent block: hashis wrong')
        
    
class Peer(Schema):
    ip = fields.Str(required=True)
    port = fields.Int(required=True)
    last_seen = fields.Int(missing=lambda: int(time()))
    
