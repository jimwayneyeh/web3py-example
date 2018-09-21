import logging.config
import yaml
import json
import datetime

from auto.infura_ropsten import w3

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
    def get_recent_blocks(self):
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

    def get_recent_transactions(self, blocks=None):
        if blocks is None:
            blocks = self.get_recent_blocks()

        transactions = list()
        for block in blocks:
            self.logger.debug('Extract transactions from block #%s...', block['number'])

            for txhash in block['transactions']:
                tx = self.w3.eth.getTransaction(txhash)
                transactions.append(tx)

        return transactions


if (__name__ == '__main__'):
    logger = logging.getLogger(__name__)

    block_reader = EthereumBlockReader(w3)

    # Print all of the transactions mined in the recent 1 minute.
    transactions = block_reader.get_recent_transactions()
    for transaction in transactions:
        logger.debug('Transaction: %s', transaction)

    '''
    Read a specific transaction by its transaction hash.
    '''
    tx = w3.eth.getTransaction('0xc3280e863f2d7cb2362ce70dfe03d4552768d36d612892c152fe6dd5761399ba')
    logger.debug('Specific transaction: %s', tx)

    # Create the contract instance in order to read the input of transaction.
    # Reference: https://ethereum.stackexchange.com/questions/20897
    with open("read_block.abi.json") as f:
        contract_abi = json.load(f)
    contract_addr = w3.toChecksumAddress('0x145b234edc704f5906d2ad0a51908ed091323098')
    my_contract = w3.eth.contract(address=contract_addr, abi=contract_abi)

    # Parse the input of the transaction.
    decoded_input = my_contract.decode_function_input(tx['input'])
    logger.debug('input: %s', decoded_input)

    # The return is a class which denotes the function. For example, here it is
    # class 'web3.utils.datatypes.startCrowdsale'.
    func_executed = decoded_input[0]

    # We can list the available members through inspect.getmembers()
    # Reference: https://stackoverflow.com/questions/1911281
    logger.debug('function name: %s', func_executed.fn_name)
