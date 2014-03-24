"""
Text parsers.
"""

from collections import namedtuple

from colorama import Fore, Style
from colorama import init
init(autoreset=True)

from utils import indent


ExecInfo = namedtuple('ExecInfo', ['return_value', 'stdout', 'stderr'])


class BasicReporter(object):

    def report(self, code, exec_info):
        """Outputs execution information to user."""
        if exec_info.return_value != 0:
            print(Fore.RED + 'Error executing code:\n')
            print(Style.BRIGHT + indent(code.encode('utf-8')))
            print('')
            print(Fore.GREEN + 'stdout:')
            print(exec_info.stdout)
            print(Fore.RED + 'stderr:')
            print(exec_info.stderr)


# List all available parsers for config-friendly usage
available = {
    'basic': BasicReporter,
    # For example:
    # 'json': JsonReporter,
}