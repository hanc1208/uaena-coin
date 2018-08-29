import datetime

from pytest import fixture
from typeguard import typechecked


@fixture
@typechecked
def fx_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


@fixture
@typechecked
def fx_timestamp(fx_now: datetime.datetime) -> int:
    return int(fx_now.timestamp() * 1000)
