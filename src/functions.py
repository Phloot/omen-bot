# src/functions.py
import os
import json

def return_config():
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'configs/config.json')

    config_json_file = open(config_path,)
    config = json.load(config_json_file)
    config_json_file.close()
    
    return config