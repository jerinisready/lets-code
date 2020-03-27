import uuid
import os
from subprocess import PIPE, run


def __save_as_file(program):
    filename = os.path.join('/tmp', (uuid.uuid4()).hex + '.py')
    with open(filename, 'w') as pointer:
        pointer.write(program)
    return filename


def __save_input(inp, filename):
    filename = filename + '.input'
    with open(filename , 'w') as pointer:
        pointer.write(inp if inp else '')
    return filename


def __unlink_files(*args):
    for filename in args:
        try:
            os.unlink(filename)
        except Exception as e:
            pass


def run_python(program, input=''):
    py_filename = __save_as_file(program)
    input_filename = __save_input(input, py_filename)
    command = ['python',  py_filename]
    infile = open(input_filename, 'r')
    result = run(command, stdout=PIPE, stderr=PIPE, stdin=infile, universal_newlines=True, shell=False)
    infile.close()
    if input_filename:
        __unlink_files(py_filename, input_filename)
    else:
        __unlink_files(py_filename)

    return result.stdout, result.stderr


__all__ = ['run_python', ]


