import os
import requests
import json
from functions import return_config

# Grab configs
config = return_config()

GW2_API_KEY = config['authentication']['gw2_token']
API_SCHEMA_VERSION = config['gw2_api_config']['schema_version']
RESPONSE_PAGE_SIZE = config['gw2_api_config']['page_size']

class APIKeyMissingError(Exception):
    pass

if not GW2_API_KEY:
    raise APIKeyMissingError(
        "Missing required API key. Please enter API key into config.json file."
    ) 

# The requests session parameters are maintained in the config.json file
# for ease of maintenance
session = requests.Session()
session.params = {}
session.params['access_token'] = GW2_API_KEY
session.params['v'] = API_SCHEMA_VERSION
session.params['page_size'] = RESPONSE_PAGE_SIZE

from .gw2_api import GW2Wrapper