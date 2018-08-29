import datetime
import decimal

from pytest import fixture
from typeguard import typechecked

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
