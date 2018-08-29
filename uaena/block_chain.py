import dataclasses
import decimal
import itertools
import time
import typing

from typeguard import typechecked

from .block import Block
from .transaction import Transaction

MINING_REWARD_SENDER = bytes.fromhex('00000000000000000000000000000000')
MINING_REWARD = decimal.Decimal('1')


@dataclasses.dataclass
class BlockChain:
    chain: typing.List[Block] = dataclasses.field(default_factory=list)
    current_transactions: typing.List[Transaction] = dataclasses.field(
        default_factory=list,
    )

    @typechecked
    def balance_of(self, address: bytes) -> decimal.Decimal:
        balance = decimal.Decimal()
        if address == MINING_REWARD_SENDER:
            return balance
        transactions = itertools.chain(
            *(block.transactions for block in self.chain),
            self.current_transactions
        )
        for transaction in transactions:
            if transaction.sender == address:
                balance -= transaction.amount
            if transaction.recipient == address:
                balance += transaction.amount
        return balance

    @typechecked
    def create_genesis_block(
        self,
        reward_recipient: bytes,
        timestamp: typing.Optional[int]=None,
    ) -> Block:
        return self.create_block(
            proof=1,
            reward_recipient=reward_recipient,
            previous_hash=bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000000'),  # noqa
            timestamp=timestamp,
        )

    @typechecked
    def create_block(
        self,
        proof: int,
        reward_recipient: bytes,
        previous_hash: typing.Optional[bytes]=None,
        timestamp: typing.Optional[int]=None,
    ) -> Block:
        """Create a new Block in the BlockChain."""
        self.append_transaction(
            Transaction(
                sender=MINING_REWARD_SENDER,
                recipient=reward_recipient,
                amount=MINING_REWARD,
            ),
        )
        block = Block(
            index=len(self.chain) + 1,
            timestamp=timestamp or int(time.time() * 1000),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.chain[-1].hash,
        )
        self.chain.append(block)
        self.current_transactions = []
        return block

    @typechecked
    def append_transaction(self, transaction: Transaction) -> int:
        """Creates a new transaction to go into the next mined Block."""
        self.valid_transaction(transaction)
        self.current_transactions.append(transaction)
        return self.last_block.index + 1 if self.last_block else 1

    @property
    @typechecked
    def last_block(self) -> typing.Optional[Block]:
        return self.chain[-1] if self.chain else None

    @typechecked
    def valid_transaction(self, transaction: Transaction):
        if transaction.sender == MINING_REWARD_SENDER:
            if transaction.amount != MINING_REWARD:
                raise ValueError(f'Mining reward must be {MINING_REWARD}')
            return
        balance = self.balance_of(transaction.sender)
        if balance < transaction.amount:
            raise ValueError(
                f'Sender {transaction.sender.hex()} does not have '
                f'sufficient balance: {transaction.amount} (have {balance})'
            )
