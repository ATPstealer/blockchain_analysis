import jsonrpclib
import datetime


class BC:
    def __init__(self):
        self.server = jsonrpclib.Server("http://weroiufn:j2340r2jrt03@91.107.224.88:8332")
        self.current_block_height = self.server.getblockcount()

    def get_block(self, block_height):
        return self.server.getblock(self.server.getblockhash(block_height))

    def get_block_date(self, block):
        """return human-readable block time"""
        return datetime.datetime.fromtimestamp(block['time'])

    def get_block_unix_date(self, block_height):
        """:return unix format block time"""
        return self.server.getblock(self.server.getblockhash(block_height))['time']

    def get_transaction(self, tx_id):
        """:return transaction data"""
        return self.server.getrawtransaction(tx_id, 1)

    def get_tx_date(self, tx):
        """:return transaction date"""
        return datetime.datetime.fromtimestamp(tx['time'])

