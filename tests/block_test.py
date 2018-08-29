from typeguard import typechecked

from uaena.block import Block


@typechecked
def test_block_serialize(fx_block: Block):
    assert fx_block.serialize() == {
        'index': 1,
        'timestamp': 737511503930,
        'proof': 1,
        'previous_hash': '0000000000000000000000000000000000000000000000000000000000000000',  # noqa
        'transactions': [
            {
                'sender': '00000000000000000000000000000000',
                'recipient': '5ca60de0575441718094ea0ffcb02aa4',
                'amount': '1',
            }
        ],
    }


@typechecked
def test_block_deserialize(fx_block: Block):
    assert Block.deserialize({
        'index': 1,
        'timestamp': 737511503930,
        'proof': 1,
        'previous_hash': '0000000000000000000000000000000000000000000000000000000000000000',  # noqa
        'transactions': [
            {
                'sender': '00000000000000000000000000000000',
                'recipient': '5ca60de0575441718094ea0ffcb02aa4',
                'amount': '1',
            }
        ],
    }) == fx_block


@typechecked
def test_block_hash(fx_block: Block):
    fx_block.timestamp = 737511503930
    assert fx_block.hash == bytes.fromhex('d9e66af21d6df26348b872c52ed4b7d054148aa5ce10d070c2463e4d59bd41bc')  # noqa
