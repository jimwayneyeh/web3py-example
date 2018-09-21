import json
import yaml
import logging.config

from auto.infura_ropsten import w3

with open('logging.yaml', 'r') as fd:
    config = yaml.safe_load(fd.read())
    logging.config.dictConfig(config)

def main ():
    logger = logging.getLogger(__name__)
    logger.debug('Is blockchain connected: %s', w3.isConnected())
    
    # Assume the contract we're going to invoke is a standard ERC20 contract.
    with open("erc20.abi.json") as f:
        erc20_abi = json.load(f)
    
    # Web3 accept only checksum address. So we should ensure the given address is a
    # checksum address before accessing the corresponding contract.
    contract_addr = w3.toChecksumAddress('0x4e470dc7321e84ca96fcaedd0c8abcebbaeb68c6')
    
    erc20_contract = w3.eth.contract(address=contract_addr, abi=erc20_abi)
    
    for func in erc20_contract.all_functions():
        logger.debug('contract functions: %s', func)
    
    logger.debug("Name of the token: %s", erc20_contract.functions.name().call())

if (__name__ == '__main__'):
    main()