import datetime
import decimal

from pytest import fixture
from typeguard import typechecked

from uaena.block import Block
from uaena.block_chain import BlockChain
from uaena.transaction import Transaction


@fixture
@typechecked
def fx_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


@fixture
@typechecked
def fx_timestamp(fx_now: datetime.datetime) -> int:
    return int(fx_now.timestamp() * 1000)


@fixture
@typechecked
def fx_transaction() -> Transaction:
    transaction = Transaction(
        sender=bytes.fromhex('5ca60de0575441718094ea0ffcb02aa4'),
        recipient=bytes.fromhex('33ee49f83681417e82660cb9585d13b1'),
        amount=decimal.Decimal('0.5'),
    )
    return transaction


@fixture
@typechecked
def fx_block() -> Block:
    block_reward = Transaction(
        sender=bytes.fromhex('00000000000000000000000000000000'),
        recipient=bytes.fromhex('5ca60de0575441718094ea0ffcb02aa4'),
        amount=decimal.Decimal('1'),
    )
    block = Block(
        index=1,
        timestamp=737511503930,  # 1993-05-16T09:18:23.930516
        proof=1,
        previous_hash=bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000000'),  # noqa
        transactions=[block_reward],
    )
    return block


@fixture
@typechecked
def fx_block_chain(
    fx_block: Block, fx_transaction: Transaction,
) -> BlockChain:
    block_chain = BlockChain(
        chain=[fx_block],
        nodes={'main.uaena.com', 'sub.uaena.com'},
    )
    block_chain.append_transaction(fx_transaction)
    block_chain.create_block(
        proof=1111,
        reward_recipient=bytes.fromhex('33ee49f83681417e82660cb9585d13b1'),
        timestamp=fx_block.timestamp + 15000,  # 1993-05-16T09:18:38.935016
    )
    block_chain.append_transaction(
        Transaction(
            sender=bytes.fromhex('33ee49f83681417e82660cb9585d13b1'),
            recipient=bytes.fromhex('a9596e7414064c778bdc36b76bb2dc2c'),
            amount=decimal.Decimal('0.25'),
        ),
    )
    return block_chain
