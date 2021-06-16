# GW2 API wrapper class
import os 
import json
from . import session

"""
GW2 API wrapper class. Configurations for endpoints are
maintained in the src/configs/config.json file for ease
of updating in the event an endpoint changes.
"""
class GW2Wrapper(object):
    def __init__(self):
        # Set OS configuration paths
        _base_dir = os.path.dirname(__file__)
        _config_path = os.path.join(_base_dir, '../configs/config.json')

        # Pull data from configuration file
        _config_json_file = open(_config_path,)
        self.config = json.load(_config_json_file)
        _config_json_file.close()

    # Internal URL builder function
    def _url_builder(self, endpoint):
        return "{0}/{1}/{2}".format(
            self.config['gw2_api_config']['api_base_path'], 
            self.config['gw2_api_config']['api_version'],
            endpoint
            ) 

    # Internal general request function
    def _api_request(self, url):
        response = session.get(url)
        return response.json()

    def worlds(self):
        return self._api_request(self._url_builder(self.config['endpoints']['worlds']))

    def wvw_matches(self):
        pass