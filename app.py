import decimal
import typing
import uuid

from flask import Flask, Response, jsonify, request
from typeguard import typechecked

from uaena.block_chain import MINING_REWARD, MINING_REWARD_SENDER, BlockChain

app = Flask(__name__)

node_identifier = str(uuid.uuid4()).replace('-', '')

block_chain = BlockChain()


@app.route('/mine/')
@typechecked
def mine() -> Response:
    last_block = block_chain.last_block
    last_proof = last_block.proof
    proof = block_chain.proof_of_work(last_proof)

    block_chain.new_transaction(
        sender=MINING_REWARD_SENDER,
        recipient=node_identifier,
        amount=MINING_REWARD,
    )

    previous_hash = last_block.hash
    block = block_chain.new_block(proof, previous_hash)

    response = {
        'message': 'New Block Forged',
        **block.serialize(),
    }

    return jsonify(response)


@app.route('/transactions/new/', methods=['POST'])
@typechecked
def new_transaction() -> typing.Tuple[typing.Union[Response, str], int]:
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    for key in required:
        return f'{key} is required', 400

    sender = values['sender']
    recipient = values['recipient']

    try:
        amount = decimal.Decimal(values['amount'])
    except TypeError:
        return f'{values["amount"]} cannot be converted to decimal', 400

    index = block_chain.new_transaction(sender, recipient, amount)

    response = {
        'message': f'Transaction will be added to Block {index}',
    }

    return jsonify(response), 201


@app.route('/chain/')
@typechecked
def full_chain() -> Response:
    response = {
        'chain': [block.serialize() for block in block_chain.chain],
        'length': len(block_chain.chain),
    }
    return jsonify(response)


@app.route('/nodes/register/', methods=['POST'])
@typechecked
def register_nodes() -> typing.Tuple[typing.Union[Response, str], int]:
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return 'Error: Please supply a valid list of nodes.', 400

    for node in nodes:
        block_chain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(block_chain.nodes),
    }

    return jsonify(response), 201


if __name__ == '__main__':
    app.run()
