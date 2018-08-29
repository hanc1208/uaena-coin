import uuid

from flask import Flask

from uaena.block_chain import BlockChain

app = Flask(__name__)

node_identifier = str(uuid.uuid4()).replace('-', '')

block_chain = BlockChain()


if __name__ == '__main__':
    app.run()
