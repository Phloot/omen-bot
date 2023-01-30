# GW2 API wrapper class
import os
import json
import logging
import requests
from functions import return_config

"""
GW2 API wrapper class. Configurations for endpoints are
maintained in the src/configs/config.json file for ease
of updating in the event an endpoint changes.
"""
class GW2Wrapper(object):
    def __init__(self, token=None):
        self.configs = return_config()
        self.logger = logging.getLogger("omen_bot_logger")

        self.headers = {
            "v": self.configs['gw2_api_config']['schema_version'],
            "page_size": self.configs['gw2_api_config']['page_size'],
            "Authorization": 'Bearer ' + token if token is not None else 'Bearer ' + self.configs['authentication']['gw2_token']
        }

    # Internal URL builder function
    def _url_builder(self, endpoint, *args, **kwargs):
        params = kwargs.get("addl_params", "")
        return f"{self.configs['gw2_api_config']['api_base_path']}/{self.configs['gw2_api_config']['api_version']}/{endpoint}{params}"

    # Internal general request function
    def _api_request(self, url):
        return requests.get(url, headers=self.headers).json()

    def account(self):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['account']))

    def objectives(self, objective):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['objectives'], addl_params=f"?id={objective}"))

    def token_info(self):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['tokeninfo']))

    # Accepts no arguments for all worlds, or list of args for 1 or more
    def worlds(self, ids: list = None):
        id_string = ','.join([str(i) for i in ids]) if ids else None
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['worlds'], addl_params="?ids=all" if not id_string else f"?ids={id_string}"))

    def wvw_matches(self, world):
        return self._api_request(self._url_builder(self.configs['gw2_endpoints']['wvw_matches'], addl_params=f"?world={world}"))


