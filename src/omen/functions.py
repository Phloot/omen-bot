# src/functions.py
import os
import sys
import json
from threading import local
import discord
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

# Function to assist in embedding local images
def attach_image(local_image_name):
    base_dir = os.path.abspath(sys.path[0])
    assets_path = os.path.join(base_dir, 'assets')
    return discord.File(os.path.join(assets_path, local_image_name), filename=local_image_name)

# Return hours, minutes, and seconds from a timedelta object
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

# Function to generate MD5 checksum of file
def md5_check(file_content):
    md5_hash = hashlib.md5()
    md5_hash.update(file_content)
    digest = md5_hash.hexdigest()
    #TODO: Add in comp against known checksums

def return_script_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Merge any given number of dictionaries
def merge_dicts(*args):
    merged = {}
    for arg in args:
        merged.update(arg)
    return merged