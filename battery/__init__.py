#! /usr/bin/env python3
# Most of this is a wrapper around battery.toml.
# If you want to know the commands, check that!
"Cross-platform battery status."

from functools import reduce
from pathlib import Path
from platform import release, system
from os import popen
from json import load
from typing import Union

def _kernel_ver():
    # pad to ensure always a 3-tuple
    rel = release().split('-')[0]
    return (tuple(map(int, rel.split('.'))) + (0, 0, 0))[:3]

def _get_os():
    if system() == 'Darwin'  and _kernel_ver() >= (6, 0, 1):  return 'macos'  # >= 10.2
    if system() == 'Linux'   and _kernel_ver() >= (2, 6, 24): return 'linux'
    if system() == 'Windows' and _kernel_ver() >= (6, 0, 0):  return 'windows'  # >= Vista
    # TODO: ios-battery maybe?  https://pypi.org/project/ios-battery
    return 'UNSUPPORTED'

def _run_command(key: str, os: Union[str, None] = None):
    os = os or _get_os()
    command = _INFO['commands'].get(os, {}).get(key, None)
    if command is None:
        raise NotImplementedError('Unknown command')
    if os == 'windows':
        command = 'powershell -c "%s"' % command
    return popen(command).read().strip()

def _chain_maybe(output, *functions):
    return reduce(lambda x, f: f(x), functions, output) if output else None

def _getter_function(typ: str, key: str):
    chain = [int]
    if typ == 'boolean':
        chain = [int, bool]
    
    def f(os: Union[str, None] = None):
        return _chain_maybe(_run_command(key, os), *chain)
    return f

__all__ = []
_COMMANDS = {}

_PATH = Path(__file__).parent / 'battery.json'
with open(_PATH) as _f:
    _INFO = load(_f)
    for _name, _f_info in _INFO['functions'].items():
        _f = _getter_function(_f_info.get('type'), _name)
        _f.__name__ = _name
        _f.__doc__ = _f_info['description']
        _COMMANDS[_name] = _f

globals().update(_COMMANDS)
__all__ = _COMMANDS.keys()