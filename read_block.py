import logging
import yaml
import datetime

with open('logging.yaml', 'r') as fd:
    config = yaml.safe_load(fd.read())
    logging.config.dictConfig(config)

class EthereumBlockReader:
    def __init__(self, w3=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)

        if w3 is None:
            raise ValueError('No web3 instance is given.')
        self.w3 = w3

    '''
    Get blocks mined in the last 1 minute.
    '''
    def getRecentBlocks(self):
        now = datetime.datetime.now()
        minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
        self.logger.debug(
            'Attempt to collect transactions between %s ~ %s.', minute_ago, now)

        # Traverse the blockchain from the latest block and collect blocks within
        # the past 1 minute.
        blocks = list()
        block_num = self.w3.eth.blockNumber
        while 1:
            block = self.w3.eth.getBlock(block_num)
            block_time = datetime.datetime.fromtimestamp(block['timestamp'])

            if block_time < minute_ago:
                self.logger.debug('Block at %s is too old.', block_time)
                break

            self.logger.info('Collect block #%s at %s', block_num, block_time)
            blocks.append(block)
            block_num -= 1

        return blocks

    def getRecentTransactions(self, blocks=None):
        if blocks is None:
            blocks = self.getRecentBlocks()

        transactions = list()
        for block in blocks:
            self.logger.debug('Extract transactions from block #%s...', block['number'])

            for txhash in block['transactions']:
                tx = self.w3.eth.getTransaction(txhash)
                transactions.append(tx)

        return transactions