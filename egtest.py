#!/usr/bin/python

"""Runs examples from text file

Usage:
  egtest.py [<filename>] [--encoding=<encoding>]
  egtest.py -h | --help
  egtest.py --version

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
  -e --encoding=<encoding>  Encoding of the input file.
"""

import os
import re
import subprocess
import sys
import tempfile

_PY3 = sys.version_info >= (3, 0)

# Constants
default_encoding = 'utf-8'
start_tag = '<test-example>'
end_tag = '</test-example>'


def main():
    from docopt import docopt
    arguments = docopt(__doc__, argv=sys.argv[1:], help=True)

    encoding = arguments['--encoding']
    if encoding is None:
        encoding = default_encoding

    # Read examples from whatever source

    filename = arguments['<filename>']
    if filename is not None:
        try:
            text = read_file(filename, encoding)
        except IOError as e:
            print('Could not open file. %s' % e)
            sys.exit(1)
    else:
        # This makes it possible to use via pipe e.g. x | python egtest.py
        text = sys.stdin.read()

    run_examples(text)


def run_examples(text):
    print 'Run examples'
    regex = re.compile('%s(.*?)%s' % (start_tag, end_tag), re.DOTALL)
    for match in re.findall(regex, text):

        run_example(match)


def run_example(example):
    code = remove_non_code(example)
    code = remove_indent(code)
    code = inject_path_append(code)

    ret_val, stdout, stderr = run_code(code)
    if ret_val != 0:
        print stdout, stderr


def remove_indent(code):
    lines = code.splitlines()
    indent = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join([x[indent:] for x in lines])


def inject_path_append(code):
    cwd = os.getcwd()
    append = u'import sys\nsys.path.insert(0, "%s")\n\n%s' % (cwd, code)
    return append


def remove_non_code(example):
    example = example.strip()
    # Remove first tag line, ```python
    # also remove ``` and tag end line from end
    return '\n'.join(example.splitlines()[2:-2])


def run_code(code):
    f, abspath = tempfile.mkstemp(suffix='.py', text=True)
    write_file(code, abspath)
    run_return = run_command(['python', abspath])

    os.remove(abspath)
    return run_return


def read_file(filepath, encoding):
    """Reads file's contents and returns unicode."""
    open_func = open
    if _PY3:
        open_func = lambda f, mode: open(f, mode, encoding=encoding)

    with open_func(filepath, 'r') as f:
        content = f.read()

    if not _PY3:
        content = content.decode(encoding, errors='replace')

    return content


def write_file(text, filepath, encoding='utf-8'):
    """Writes unicode to file with specified encoding."""
    open_func = open
    if _PY3:
        open_func = lambda f, mode: open(f, mode, encoding=encoding)
    else:
        text = text.encode(encoding, errors='replace')

    with open_func(filepath, 'w') as f:
        f.write(text)


def run_command(command):
    """Runs an command and returns the stdout and stderr as a string.

    Args:
        command: Command to execute in Popen's list format.
                 E.g. ['ls', '..']

    Returns:
        tuple. (return_value, stdout, stderr), where return_value is the
        numerical exit code of process and stdout/err are strings containing
        the output. stdout/err is None if nothing has been output.
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return_value = p.wait()
    return return_value, stdout, stderr


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit.')
