from typing import List
import json


def get_config():
    try:
        f = open('./vrc-discord-osc.config.json')
        data = json.load(f)
        f.close()
        print("Custom config file found!")
        return data
    except:
        pass


def get_port_number(config) -> int:
    port = 9000
    if config is None:
        return port
    if ("port" in config):
        if type(config['port']) is int:
            print(f"Using port {config['port']}.")
            port = config['port']
    return port


def get_username_allow_list(config) -> List[str]:
    username_allow_list: List[str] = []
    if config is None:
        return username_allow_list
    if ("username_allow_list" in config):
        if type(config['username_allow_list']) is list:
            print(
                f"Using username_allow_list {config['username_allow_list']}.")
            username_allow_list = config['username_allow_list']
    return username_allow_list
