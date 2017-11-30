from json import loads
from pathlib import Path

from flask import current_app
from application import VERSION


_health_check = {}

if Path('git_info').exists():
    with open('git_info') as io:
        _health_check = loads(io.read())


def get_info():
    info = {
        "name": current_app.config['NAME'],
        "version": VERSION,
    }
    info = dict(_health_check, **info)

    return info
