import os
from optparse import OptionParser

from . import pytemplate

def define_cli_args():
    parser = OptionParser()
    parser.add_option("-m", "--module", dest="module", default=None,
                      help="Module name")
    parser.add_option("-e", "--exec", dest="executable", default=None,
                      help="Executable name")
    parser.add_option("-l", "--library", dest="lib", default=None,
                      help="Entry point python script file name")

    return parser.parse_args()


def main():
    (options, args) = define_cli_args()
    pytemplate.main(options)
