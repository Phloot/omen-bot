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
<<<<<<< HEAD
        self.logger = logging.getLogger("oasis_bot_logger")

    # Internal URL builder function
    def _url_builder(self, endpoint, *args, **kwargs):
        params = kwargs.get("addl_params", "")
        return "{0}/{1}/{2}{3}".format(
            self.configs['gw2_api_config']['api_base_path'], 
            self.configs['gw2_api_config']['api_version'],
            endpoint,
            params
=======

    # Internal URL builder function
    def _url_builder(self, endpoint):
        return "{0}/{1}/{2}".format(
            self.configs['gw2_api_config']['api_base_path'], 
            self.configs['gw2_api_config']['api_version'],
            endpoint
>>>>>>> 0d10d75befd576c4faf79e842aaad44b4476add9
            ) 

    # Internal general request function
    def _api_request(self, url):
        response = session.get(url)
        return response.json()

    def worlds(self):
<<<<<<< HEAD
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['worlds'], addl_params="?ids=all"))
=======
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['worlds']))
>>>>>>> 0d10d75befd576c4faf79e842aaad44b4476add9

    def wvw_matches(self):
        pass