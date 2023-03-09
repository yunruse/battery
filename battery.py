#! /usr/bin/env python3
# Most of this is a wrapper around battery.toml.
# If you want to know the commands, check that!
"Cross-platform battery status."

from functools import reduce
from platform import release, system
from os import popen
from json import dumps, load

def _kernel_ver():
    # pad to ensure always a 3-tuple
    return (tuple(map(int, release().split('.'))) + (0, 0, 0))[:3]

def _get_os():
    if system() == 'Darwin'  and _kernel_ver() >= (6, 0, 1):  return 'macos'  # >= 10.2
    if system() == 'Linux'   and _kernel_ver() >= (2, 6, 24): return 'linux'
    if system() == 'Windows' and _kernel_ver() >= (6, 0, 0):  return 'windows'  # >= Vista
    return 'UNSUPPORTED'

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
    chain = [int]
    if typ == 'boolean':
        chain = [int, bool]
    
    def f(os: str = None):
        return chain_maybe(_run_command(key, os), *chain)
    return f

__all__ = []
COMMANDS = {}

PATH = __file__.replace('.py', '.json')
with open(PATH) as f:
    INFO = load(f)
    for name, f_info in INFO['functions'].items():
        f = _getter_function(f_info.get('type'), name)
        f.__name__ = name
        f.__doc__ = f_info['description']
        COMMANDS[name] = f

globals().update(COMMANDS)
__all__ = COMMANDS.keys()
OSES = INFO['commands'].keys()

if __name__ == '__main__':
    from argparse import ArgumentParser, RawTextHelpFormatter

    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)

    FUNCTIONS = '\n'.join(
        '- {:<24} {}'.format('`{}`:'.format(k), v['description'])
        for k, v in INFO['functions'].items())

    parser.add_argument(
        'info', choices=__all__, metavar='FUNC', default=None, nargs='?',
        help='The information to obtain. Leave blank for a JSON of all info items.'
        ' The available info keys are:\n' + FUNCTIONS)

    parser.add_argument(
        '--command', '-c', action='store_true',
        help='Print the Terminal or PowerShell command used on this OS.')

    parser.add_argument(
        '--os', choices=OSES, metavar='OS', default=None,
        help='Override the operating system. One of: ' + ', '.join(OSES))
    
    args = parser.parse_args()

    def sanitise(command):
        return command.replace('\n', '\\n')

    def _get_key(key):
        os = args.os or _get_os()
        if key not in INFO['commands'].get(os, {}):
            exit(4)
        if args.command:
            return sanitise(INFO['commands'][os][key])
        else:
            return COMMANDS[key](os=os)
    
    if args.info is None:
        print(dumps({k: _get_key(k) for k in COMMANDS.keys()}))
    else:
        print(_get_key(args.info))