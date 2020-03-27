import uuid
import os
from subprocess import PIPE, run, Popen


def __save_as_file(program):
    filename = os.path.join('/tmp', (uuid.uuid4()).hex + '.py')
    with open(filename, 'w') as pointer:
        pointer.write(program)
    return filename


def __save_input(inp, filename):
    filename = filename + '.input'
    with open(filename, 'w') as pointer:
        pointer.write(inp if inp else '')
    return filename


def __unlink_files(*args):
    for filename in args:
        try:
            os.unlink(filename)
        except Exception as e:
            pass


def run_python(program, inp=''):
    py_filename = __save_as_file(program)
    input_filename = __save_input(inp, py_filename)
    command = ['python3',  py_filename]

    fopen = open(input_filename, 'r')
    result = run(command, stdout=PIPE, stderr=PIPE, stdin=fopen)
    fopen.close()
    if input_filename:
        __unlink_files(py_filename, input_filename)
    else:
        __unlink_files(py_filename)

    return result.stdout, result.stderr


__all__ = ['run_python', ]


