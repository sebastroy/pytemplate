"""
    main entrypoint boilerplate
"""
import argparse
import sys

from .__version__ import __version__
from .__description__ import __description__
from .pytemplate import pytemplate


def valid_args(args):
    """ further args validation """
    print(args.exec)
    if args.exec is not None:
        for exc in args.exec:
            if ':' not in exc:
                return False
        clis = set()
        funcs = set()
        for word in args.exec:
            cli, func = word.split(':')
            if cli in clis:
                print(cli, 'is not unique')
                return False
            if func in funcs:
                print(func, 'is not unique')
                return False
            clis.add(cli)
            funcs.add(func)
    return True


def main_argparse():
    """
        argparse boilerplate code
        - Add relevant options
        - in case you have multiple entrypoints with different argparse
          args lists, use the parent functionality from argparse
          see https://docs.python.org/3/library/argparse.html
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__)

    parser.add_argument('-m', '--module',
                        action='store',
                        nargs=1,
                        type=str,
                        required=True,
                        help='name of the package',
                        metavar='<module name>')
    parser.add_argument('-l', '--library',
                        action='store',
                        nargs=1,
                        type=str,
                        help='name of the main library if different from package name',
                        metavar='<library name>')
    parser.add_argument('-e', '--exec',
                        action='append',
                        type=str,
                        help='name of entrypoint if any',
                        metavar='<executable name>:<function name>')
    parser.add_argument('-d', '--description',
                        action='store',
                        nargs=1,
                        type=str,
                        help='description for module',
                        default='noop')

    args = parser.parse_args()
    if valid_args(args):
        return args
    parser.print_help()
    sys.exit(1)


def main():
    """ main passover """
    args = main_argparse()
    pytemplate(args)
