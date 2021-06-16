import os
import requests
import json

# Set OS configuration paths
base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, '../configs/config.json')

# Pull data from configuration file
config_json_file = open(config_path,)
config = json.load(config_json_file)
config_json_file.close()

GW2_API_KEY = config['authentication']['gw2_token']
API_SCHEMA_VERSION = config['gw2_api']['schema_version']
RESPONSE_PAGE_SIZE = config['gw2_api']['page_size']

class APIKeyMissingError(Exception):
    pass

if not GW2_API_KEY:
    raise APIKeyMissingError(
        "Missing required API key. Please enter API key into config.json file."
    ) 

session = requests.Session()
session.params = {}
session.params['access_token'] = GW2_API_KEY
session.params['v'] = API_SCHEMA_VERSION
session.params['page_size'] = RESPONSE_PAGE_SIZE

from .gw2_api import GW2Wrapper