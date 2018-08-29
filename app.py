import uuid

from flask import Flask, Response, jsonify
from typeguard import typechecked

from uaena.block_chain import BlockChain

app = Flask(__name__)

node_identifier = str(uuid.uuid4()).replace('-', '')

block_chain = BlockChain()


@app.route('/chain/')
@typechecked
def full_chain() -> Response:
    response = {
        'chain': [block.serialize() for block in block_chain.chain],
        'length': len(block_chain.chain),
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
