from json import loads
from pathlib import Path

from application import __version__


_health_check = {}

if Path('git_info').exists():
    with open('git_info') as io:
        _health_check = loads(io.read())


def get_info():
    info = {
        "name": 'rm-comms-template',
        "version": __version__,
    }
    info = dict(_health_check, **info)

    return info
