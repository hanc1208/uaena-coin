from __future__ import annotations

import dataclasses
import hashlib
import json
import typing

from typeguard import typechecked

from .transaction import Transaction


@dataclasses.dataclass
class Block:
    index: int
    timestamp: int
    proof: int
    previous_hash: bytes
    transactions: typing.List[Transaction] = dataclasses.field(
        default_factory=list,
    )

    @typechecked
    def serialize(self) -> typing.Mapping[str, typing.Any]:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof': self.proof,
            'previous_hash': self.previous_hash.hex(),
            'transactions': [t.serialize() for t in self.transactions],
        }

    @staticmethod
    @typechecked
    def deserialize(data: typing.Mapping[str, typing.Any]) -> Block:
        return Block(
            index=int(data['index']),
            timestamp=int(data['timestamp']),
            proof=int(data['proof']),
            previous_hash=bytes.fromhex(data['previous_hash']),
            transactions=[
                Transaction.deserialize(transaction)
                for transaction in data['transactions']
            ],
        )

    @property
    @typechecked
    def hash(self) -> bytes:
        """Creates a SHA-256 hash of a Block"""
        block_string = json.dumps(self.serialize(), sort_keys=True).encode()
        return bytes.fromhex(hashlib.sha256(block_string).hexdigest())
