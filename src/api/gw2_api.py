# GW2 API wrapper class
import os 
import json
from . import session
from functions import return_config

"""
GW2 API wrapper class. Configurations for endpoints are
maintained in the src/configs/config.json file for ease
of updating in the event an endpoint changes.
"""
class GW2Wrapper(object):
    def __init__(self):
        self.configs = return_config()
        logger = logging.getLogger("oasis_bot_logger")

    # Internal URL builder function
    def _url_builder(self, endpoint):
        return "{0}/{1}/{2}".format(
            self.configs['gw2_api_config']['api_base_path'], 
            self.configs['gw2_api_config']['api_version'],
            endpoint
            ) 

    # Internal general request function
    def _api_request(self, url):
        response = session.get(url)
        return response.json()

    def worlds(self):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['worlds']))

    def wvw_matches(self):
        pass