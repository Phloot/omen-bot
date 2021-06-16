# GW2 API wrapper class
import os 
import json
from . import session

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
        return "{0}/{1}".format(
            self.config['gw2_api']['api_base_path'], 
            self.config['gw2_api']['api_version']
            ) 

    def wvw_matches(self):
        pass