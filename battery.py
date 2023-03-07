#! /usr/bin/env python3
"Cross-platform battery status."

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

def _run_command(command: str):
    if _get_os() == 'windows':
        command = 'powershell -c "%s"' % command
    return popen(command).read().strip()

def _getter_function(typ: str, command: str):
    if command is None:
        def f(): return NotImplemented
    elif typ == 'number':
        def f(): return int(_run_command(command))
    elif typ == 'boolean':
        def f(): return bool(int(_run_command(command)))
    return f

__all__ = []
COMMANDS = {}

with open('battery.json') as f:
    INFO = load(f)
    for name, f_info in INFO['functions'].items():
        command = INFO['commands'].get(_get_os(), {}).get(name, None)
        f = _getter_function(f_info['type'], command)
        f.__name__ = name
        f.__doc__ = f_info['description']
        COMMANDS[name] = f

globals().update(COMMANDS)
__all__ = COMMANDS.keys()

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)

    parser.add_argument(
        'info', nargs='?', choices=__all__, default=None,
        help='The information to obtain. Leave blank for a JSON of all info items.')

    parser.add_argument(
        '--command', '-c', action='store_true',
        help='Print the command used, instead of its result.')
    
    args = parser.parse_args()

    def _get_key(key):
        if key not in INFO['commands'].get(_get_os(), {}):
            exit(4)
        
        if args.command:
            return INFO['commands'][_get_os()][key]
        else:
            return COMMANDS[key]()
    
    if args.info is None:
        print({k: _get_key(k) for k in COMMANDS.keys()})
    else:
        print(_get_key(args.info))