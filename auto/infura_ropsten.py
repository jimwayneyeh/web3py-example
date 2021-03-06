import logging
import os

from web3 import (
    HTTPProvider,
    Web3,
)

INFURA_ROPSTEN_BASE_URL = 'https://ropsten.infura.io/v3'

def load_infura_url():
    key = os.environ.get('INFURA_API_KEY', '')
    if key == '':
        logging.getLogger('auto.infura_ropsten').warning(
            "No Infura API Key found. Add environment variable INFURA_API_KEY to ensure continued "
            "API access. New keys are available at https://infura.io/signup"
        )
        return INFURA_ROPSTEN_BASE_URL
    else:
        return "%s/%s" % (INFURA_ROPSTEN_BASE_URL, key)

w3 = Web3(HTTPProvider(load_infura_url()))