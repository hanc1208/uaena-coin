import datetime
import decimal

from pytest import fixture
from typeguard import typechecked

from uaena.block import Block
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
