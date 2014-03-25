"""
Text parsers.
"""

import json

from colorama import Fore, Style
from colorama import init
init(autoreset=True)

from utils import indent


class ExecInfo(object):
    def __init__(self, return_value, stdout, stderr):
        self.return_value = return_value
        self.stdout = stdout
        self.stderr = stderr


class BasicReporter(object):

    def __init__(self, blocks):
        """
        blocks: code blocks to be executed
        """
        self._blocks = blocks
        print('Testing %s example(s)..\n' % len(self._blocks))

    def on_execute(self, code_info, exec_info):
        """
        Outputs execution information to user.
        """
        if exec_info.return_value != 0:
            print(Fore.RED + 'Error executing code:\n')
            print(Style.BRIGHT + indent(code_info.code.encode('utf-8')))
            print('')
            print(Fore.GREEN + 'stdout:')
            print(exec_info.stdout)
            print(Fore.RED + 'stderr:')
            print(exec_info.stderr)
            print(Style.BRIGHT + '---------------------\n')

    def on_finish(self, exec_infos, success):
        """
        exec_infos: List of ExecInfo objects. Contains all executions.
        """
        if success:
            print(Fore.GREEN + '\nSUCCESS')
        else:
            print(Fore.RED + '\nFAILURE')


class JsonReporter(object):

    def __init__(self, blocks):
        """
        blocks: code blocks to be executed
        """
        self._blocks = blocks

    def on_execute(self, code_info, exec_info):
        if exec_info.return_value != 0:
            print(Fore.RED + 'Error executing code:\n')
            print(Style.BRIGHT + indent(code_info.code.encode('utf-8')))
            print('')
            print(Fore.GREEN + 'stdout:')
            print(exec_info.stdout)
            print(Fore.RED + 'stderr:')
            print(exec_info.stderr)
            print(Style.BRIGHT + '---------------------\n')

    def on_finish(self, exec_infos, success):
        if success:
            print(Fore.GREEN + '\nSUCCESS')
        else:
            print(Fore.RED + '\nFAILURE')


# List all available parsers for config-friendly usage
available = {
    'basic': BasicReporter,
    # For example:
    # 'json': JsonReporter,
}
