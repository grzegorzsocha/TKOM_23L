from interpreter.interpreter import Interpreter
from argparse import ArgumentParser
import sys


def main(args):
    parser = ArgumentParser(prog='Interpreter', description='Interpreter for my fantastic language')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str, help='Run interpreter using file')
    group.add_argument('-s', '--string', type=str, help='Run interpreter using string')
    arguments = parser.parse_args(args)

    if arguments.file:
        interpreter = Interpreter(True, arguments.file)
    else:
        interpreter = Interpreter(False, arguments.string)

    interpreter.run()


if __name__ == '__main__':
    main(sys.argv[1:])
