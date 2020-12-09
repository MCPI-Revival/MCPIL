import json

from pathlib import Path

def _get_config_path() -> str:
    return str(Path.home()) + '/.mcpil.json'

def _copy(src: dict, dst: dict):
    for key in dst:
        if key in src and type(src[key]) is type(dst[key]):
            if isinstance(dst[key], dict):
                _copy(src[key], dst[key])
            else:
                dst[key] = src[key]

def load() -> dict:
    obj: dict
    try:
        with open(_get_config_path(), 'r') as file:
            obj = json.load(file)
    except json.JSONDecodeError as e:
        obj = {}
    out = {'general': {'custom-features': [], 'username': 'StevePi'}, 'server': {'ip': '', 'port': ''}}
    _copy(obj, out)
    return out

def save(obj: dict):
    with open(_get_config_path(), 'w') as file:
        json.dump(obj, file)
