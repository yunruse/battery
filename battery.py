#! /usr/bin/env python3
"Cross-platform battery status."

from functools import reduce
from platform import system
from os import popen
from json import load

def _get_os():
    if system() == 'Darwin':
        return 'macos'
    if system() == 'Windows':
        # TODO: ignore XP and below
        return 'windows'
    return 'unknown'

def _run_command(key: str, os: str = None):
    os = os or _get_os()
    command = INFO['commands'].get(os, {}).get(key, None)
    if command is None:
        raise NotImplementedError('Unknown command')
    if os == 'windows':
        command = 'powershell -c "%s"' % command
    return popen(command).read().strip()

def chain_maybe(output, *functions):
    return reduce(lambda x, f: f(x), functions, output) if output else None

def _getter_function(typ: str, key: str):
    chain = []
    if typ == 'number':
        chain = [int]
    elif typ == 'boolean':
        chain = [int, bool]
    
    def f(os: str = None):
        return chain_maybe(_run_command(key, os), *chain)
    return f

__all__ = []
COMMANDS = {}

with open('battery.json') as f:
    INFO = load(f)
    for name, f_info in INFO['functions'].items():
        f = _getter_function(f_info['type'], name)
        f.__name__ = name
        f.__doc__ = f_info['description']
        COMMANDS[name] = f

globals().update(COMMANDS)
__all__ = COMMANDS.keys()
OSES = INFO['commands'].keys()

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        'info', nargs='?', choices=__all__, default=None,
        help='The information to obtain. Leave blank for a JSON of all info items.')

    parser.add_argument(
        '--command', '-c', action='store_true',
        help='Print the Terminal or PowerShell command used instead of its result.')

    parser.add_argument(
        '--os', nargs='?', choices=OSES, default=None,
        help='Override the operating system.')
    
    args = parser.parse_args()

    def _get_key(key):
        os = args.os or _get_os()
        if key not in INFO['commands'].get(os, {}):
            exit(4)
        if args.command:
            return repr(INFO['commands'][os][key])[1:-1]
        else:
            return COMMANDS[key](os=os)
    
    if args.info is None:
        print({k: _get_key(k) for k in COMMANDS.keys()})
    else:
        print(_get_key(args.info))