from __future__ import annotations

import dataclasses
import decimal
import typing

from typeguard import typechecked


@dataclasses.dataclass
class Transaction:
    sender: bytes
    recipient: bytes
    amount: decimal.Decimal

    @typechecked
    def serialize(self) -> typing.Mapping[str, typing.Any]:
        return {
            'sender': self.sender.hex(),
            'recipient': self.recipient.hex(),
            'amount': str(self.amount),
        }

    @staticmethod
    @typechecked
    def deserialize(data: typing.Mapping[str, typing.Any]) -> Transaction:
        return Transaction(
            sender=bytes.fromhex(data['sender']),
            recipient=bytes.fromhex(data['recipient']),
            amount=decimal.Decimal(data['amount']),
        )
