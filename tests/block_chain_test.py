import decimal

from pytest import raises
from typeguard import typechecked

from uaena.block import Block
from uaena.block_chain import BlockChain
from uaena.transaction import Transaction


@typechecked
def test_block_chain_balance_of(fx_block_chain: BlockChain):

    def balance_of(address: str):
        return fx_block_chain.balance_of(bytes.fromhex(address))

    assert balance_of('00000000000000000000000000000000') == 0
    assert balance_of('5ca60de0575441718094ea0ffcb02aa4') == 0.5
    assert balance_of('33ee49f83681417e82660cb9585d13b1') == 1.25
    assert balance_of('a9596e7414064c778bdc36b76bb2dc2c') == 0.25


@typechecked
def test_block_chain_create_genesis_block():
    block_chain = BlockChain()
    block_chain.create_genesis_block(
        reward_recipient=bytes.fromhex('5ca60de0575441718094ea0ffcb02aa4'),
        timestamp=737511503930,  # 1993-05-16T09:18:23.930516
    )
    assert block_chain.chain == [
        Block(
            index=1,
            timestamp=737511503930,
            previous_hash=bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000000'),  # noqa
            proof=1,
            transactions=[
                Transaction(
                    sender=bytes.fromhex('00000000000000000000000000000000'),
                    recipient=bytes.fromhex('5ca60de0575441718094ea0ffcb02aa4'),
                    amount=decimal.Decimal('1'),
                ),
            ],
        ),
    ]
    assert block_chain.current_transactions == []


@typechecked
def test_block_chain_create_block(fx_block_chain: BlockChain):
    transaction = Transaction(
        sender=bytes.fromhex('a9596e7414064c778bdc36b76bb2dc2c'),
        recipient=bytes.fromhex('619b9000222b457b978efbca2815d38a'),
        amount=decimal.Decimal('0.125'),
    )
    fx_block_chain.append_transaction(transaction)
    block = fx_block_chain.create_block(
        proof=1234,
        reward_recipient=bytes.fromhex('619b9000222b457b978efbca2815d38a'),
        timestamp=fx_block_chain.last_block.timestamp + 15000,
    )
    assert fx_block_chain.chain[-1] == block
    assert block.index == 3
    assert block.timestamp == 737511533930
    assert len(block.transactions) == 3
    assert transaction in block.transactions
    assert block.proof == 1234
    assert block.previous_hash == bytes.fromhex('46e136b65129b85429f25d777cb20c4c44d91ae46e18b6f540c45135d340c2cb')  # noqa
    assert not fx_block_chain.current_transactions
    assert fx_block_chain.balance_of(
        bytes.fromhex('a9596e7414064c778bdc36b76bb2dc2c')
    ) == 0.125
    assert fx_block_chain.balance_of(
        bytes.fromhex('619b9000222b457b978efbca2815d38a')
    ) == 1.125


@typechecked
def test_block_chain_append_transaction(fx_block_chain: BlockChain):
    transaction = Transaction(
        sender=bytes.fromhex('a9596e7414064c778bdc36b76bb2dc2c'),
        recipient=bytes.fromhex('619b9000222b457b978efbca2815d38a'),
        amount=decimal.Decimal('0.125'),
    )
    assert fx_block_chain.append_transaction(transaction) == 3
    assert len(fx_block_chain.current_transactions) == 2
    assert transaction in fx_block_chain.current_transactions

    invalid_transaction = Transaction(
        sender=bytes.fromhex('00000000000000000000000000000000'),
        recipient=bytes.fromhex('619b9000222b457b978efbca2815d38a'),
        amount=decimal.Decimal('0.00000001'),
    )
    with raises(ValueError) as e:
        fx_block_chain.append_transaction(invalid_transaction)
    assert str(e.value) == 'Mining reward must be 1'


@typechecked
def test_block_chain_last_block(fx_block_chain: BlockChain):
    assert fx_block_chain.last_block.index == 2
    assert fx_block_chain.last_block.hash == bytes.fromhex('46e136b65129b85429f25d777cb20c4c44d91ae46e18b6f540c45135d340c2cb')  # noqa

    fx_block_chain.chain = []
    assert fx_block_chain.last_block is None


@typechecked
def test_block_chain_valid_transaction(fx_block_chain: BlockChain):
    invalid_reward_amount_transaction = Transaction(
        sender=bytes.fromhex('00000000000000000000000000000000'),
        recipient=bytes.fromhex('619b9000222b457b978efbca2815d38a'),
        amount=decimal.Decimal('0.00000001'),
    )
    with raises(ValueError) as e:
        fx_block_chain.valid_transaction(invalid_reward_amount_transaction)
    assert str(e.value) == 'Mining reward must be 1'

    lack_of_balance_transaction = Transaction(
        sender=bytes.fromhex('a9596e7414064c778bdc36b76bb2dc2c'),
        recipient=bytes.fromhex('619b9000222b457b978efbca2815d38a'),
        amount=decimal.Decimal('10000000'),
    )
    with raises(ValueError) as e:
        fx_block_chain.valid_transaction(lack_of_balance_transaction)
    assert str(e.value) == (
        'Sender a9596e7414064c778bdc36b76bb2dc2c '
        'does not have sufficient balance: 10000000 (have 0.25)'
    )


@typechecked
def test_block_chain_valid_proof():
    assert not BlockChain.valid_proof(1234, 62593)
    assert BlockChain.valid_proof(1234, 62594)
    assert not BlockChain.valid_proof(1234, 62595)


@typechecked
def test_block_chain_proof_of_work():
    assert True
