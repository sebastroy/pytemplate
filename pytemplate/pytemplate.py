import os


MAKEFILE = [
        'UNIT_DIR = test',
        'TMP = build',
        'VERSION := $(shell python3 setup.py --version)',
        '',
        '.PHONY: all',
        'all:',
        '',
        '.PHONY: clean',
        'clean:',
        '	rm -rf $(TMP)',
        '',
        '.PHONY: sdist',
        'sdist:',
        '	mkdir -p $(TMP)',
        '	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST',
        '',
        '.PHONY: test',
        'test: unit',
        '',
        '.PHONY: unit',
        'unit:',
        '	python3 -munittest discover -s $(UNIT_DIR) $(TESTOPTS)',
        '',
        '.PHONY: upload',
        'upload: unit',
        '	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST upload'
        ]

INIT_ENV = [
        '#!/bin/bash',
        '',
        'export PLATFORM=$(uname)',
        'export PIP_CMD="python3 -m pip"',
        'export ANCHOR_POINT=$(pwd)',
        '',
        'to_anchor() {',
        '  cd $ANCHOR_POINT',
        '}',
        '',
        'install_dependencies() {',
        '  $PIP_CMD install --upgrade pip',
        '  $PIP_CMD install --upgrade -r requirements.txt',
        '  [ -d src ] && (cd src && for i in */requirements.txt; do $PIP_CMD install -r $i; done)',
        '}',
        '',
        'create_venv() {',
        '  python3 -m venv ./venv/${PLATFORM} # assume python version is at least 3.4',
        '}',
        '',
        '[ ! -e ./venv/${PLATFORM}/bin/activate ] && create_venv && . ./venv/${PLATFORM}/bin/activate && install_dependencies',
        '[ ! -e ./venv/${PLATFORM}/bin/activate ] || . ./venv/${PLATFORM}/bin/activate',
        ]


def yield_bin(module):
    return '\n'.join([
        '#!/usr/bin/env python',
        '',
        'from ' + module + '.__main__ import main',
        '',
        'if __name__ == \'__main__\':',
        '    main()'
        ])


def yield_init(lib):
    return '\n'.join([
        'from .__version__ import version as __version__',
        'from . import ' + lib
        ])


def yield_main(lib):
    return '\n'.join([
        'from optparse import OptionParser',
        '',
        'from . import ' + lib,
        '',
        'def define_cli_args():',
        '    parser = OptionParser()',
        '    # read file',
        '    parser.add_option("-j", "--json-file", dest="infile", default="data.json",',
        '                      help="name of json format input route file", metavar="FILE")',
        '    # write file',
        '    parser.add_option("-s", "--sol-file", dest="outfile", default="sol.json",',
        '                      help="name of json format output route file", metavar="FILE")',
        '    # flags',
        '    parser.add_option("-a", "--write-allout", action="store_true", dest="allformat", default=False,',
        '                      help="write output to all format")',
        '    parser.add_option("-n", "--no-run", action="store_true", dest="norun", default=False,',
        '                      help="do not run solving")',
        '',
        '    return parser.parse_args()',
        '',
        '',
        'def main():',
        '    (options, args) = define_cli_args()',
        '    ' + lib + '.main(options)',
        ])


def yield_lib():
    return '\n'.join([
        '',
        '',
        '',
        'def main(options):',
        '    pass'
        ])


def yield_makefile():
    return '\n'.join(MAKEFILE)


def yield_init_env():
    return '\n'.join(INIT_ENV)


def yield_setup(module, escript):
    return '\n'.join([
        'from distutils.core import setup',
        'import os',
        '',
        'description = "DESCRIPTION"',
        '',
        'long_description = (',
        ')',
        '',
        'def get_version():',
        '    for line in open(\'' + module + '/__version__.py\'):',
        '        if \'version\' in line:',
        '            return line.split(\'=\')[1].strip(\' \\n\\\'\"\')',
        '    raise Error("No version")',
        '',
        'setup(',
        '    author="Sebastien Roy",',
        '    author_email="sebastien.roy.sr@gmail.com",',
        '    classifiers=[',
        '        "Environment :: Console",',
        '        "Programming Language :: Python",',
        '        "Topic :: Office/Business",',
        '        "Topic :: Utilities"',
        '    ],',
        '    description=description,',
        '    long_description=long_description,',
        '    name=\'' + module + '\',',
        '    packages=[\'' + module + '\'],',
        '    scripts=[',
        '            os.path.join(\'bin\', "' + escript + '"),',
        '        ],',
        '    version=get_version(),',
        '    install_requires=[',
        '        ]',
        ')',
        ])


def write_file(name, content):
    with open(name, 'w+') as f:
        f.write(content)
    f.close()


def main(options):
    if options.module is None:
        raise RuntimeError('error: module name not provided')

    module = options.module
    escript = options.executable or module
    lib = options.lib or module

    os.makedirs(module)
    os.makedirs('bin')

    write_file(os.path.join('bin', escript), yield_bin(module))
    write_file('README.md', '')
    write_file('requirements.txt', '')
    write_file(os.path.join(module, '__version__.py'), 'version = \'0.1\'')
    write_file(os.path.join(module, '__init__.py'), yield_init(lib))
    write_file(os.path.join(module, '__main__.py'), yield_main(lib))
    write_file(os.path.join(module, lib + '.py'), yield_lib())
    write_file('Makefile', yield_makefile())
    write_file('init_env', yield_init_env())
    write_file('setup.py', yield_setup(module, escript))
    write_file('MANIFEST.in', 'include README.md VERSION')
    write_file('.gitignore', '*.egg-info\n__pycache__\n')
    print("module created")
    print("do not forget to add package list in requirements.txt AND setup.py if any")
    print("\"pip install -e .\" to initial dev install and \"pip install -e <path> --upgrade\" if you ever add more bin exec")



#git init .
#git add .
#git commit -m "initial commit"

