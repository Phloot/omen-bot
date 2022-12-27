# GW2 API wrapper class
import os 
import json
import logging
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
        self.logger = logging.getLogger("omen_bot_logger")

    # Internal URL builder function
    def _url_builder(self, endpoint, *args, **kwargs):
        params = kwargs.get("addl_params", "")
        return f"{self.configs['gw2_api_config']['api_base_path']}/{self.configs['gw2_api_config']['api_version']}/{endpoint}{params}"

    # Internal general request function
    def _api_request(self, url):
        return session.get(url).json()

    def account(self):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['account']))

    def worlds(self):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['worlds'], addl_params="?ids=all"))

    def wvw_matches(self):
        pass
