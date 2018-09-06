import json
import yaml
import logging.config

from web3.auto.infura import w3

with open('logging.yaml', 'r') as fd:
    config = yaml.safe_load(fd.read())
    logging.config.dictConfig(config)

def main ():
    logger = logging.getLogger(__name__)
    
    logger.debug('is connected: %s', w3.isConnected())

if (__name__ == '__main__'):
    main()