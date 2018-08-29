from typeguard import typechecked

from uaena.transaction import Transaction


@typechecked
def test_transaction_serialize(fx_transaction: Transaction):
    assert fx_transaction.serialize() == {
        'sender': '5ca60de0575441718094ea0ffcb02aa4',
        'recipient': '33ee49f83681417e82660cb9585d13b1',
        'amount': '0.5',
    }


@typechecked
def test_transaction_deserialize(fx_transaction: Transaction):
    assert Transaction.deserialize({
        'sender': '5ca60de0575441718094ea0ffcb02aa4',
        'recipient': '33ee49f83681417e82660cb9585d13b1',
        'amount': '0.5',
    }) == fx_transaction
