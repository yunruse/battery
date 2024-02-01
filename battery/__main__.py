from json import dumps
from argparse import ArgumentParser, RawTextHelpFormatter

from . import _INFO, __all__, _get_os, _COMMANDS

parser = ArgumentParser(
    description="Cross-platform battery status.",
    formatter_class=RawTextHelpFormatter)

_OSES = _INFO['commands'].keys()
FUNCTIONS = '\n'.join(
    '- {:<24} {}'.format('`{}`:'.format(k), v['description'])
    for k, v in _INFO['functions'].items())

parser.add_argument(
    'info', choices=__all__, metavar='FUNC', default=None, nargs='?',
    help='The information to obtain. Leave blank for a JSON of all info items.'
    ' The available info keys are:\n' + FUNCTIONS)

parser.add_argument(
    '--command', '-c', action='store_true',
    help='Print the Terminal or PowerShell command used on this OS.')

parser.add_argument(
    '--os', choices=_OSES, metavar='OS', default=None,
    help='Override the operating system. One of: ' + ', '.join(_OSES))

args = parser.parse_args()

def _get_key(key):
    os = args.os or _get_os()
    if key not in _INFO['commands'].get(os, {}):
        exit(4)
    if args.command:
        return _INFO['commands'][os][key].replace('\n', '\\n')
    else:
        return _COMMANDS[key](os=os)

if args.info is None:
    print(dumps({k: _get_key(k) for k in _COMMANDS.keys()}))
else:
    print(dumps(_get_key(args.info)))
