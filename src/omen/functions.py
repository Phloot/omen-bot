# src/functions.py
import os
import json
import logging
import hashlib

logger = logging.getLogger("omen_bot_logger")

# Reusable function to pull in config
def return_config():
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'configs', 'config.json')

    config_json_file = open(config_path,)
    config = json.load(config_json_file)
    config_json_file.close()

    return config

# Helper function to convert args to lowercase
def to_lower(argument):
    return argument.lower()

# Function to generate MD5 checksum of file
def md5_check(file_content):
    md5_hash = hashlib.md5()
    md5_hash.update(file_content)
    digest = md5_hash.hexdigest()
    #TODO: Add in comp against known checksums
