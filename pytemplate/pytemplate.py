"""
This library implements a python package generator complying to
PyPA standard using setuptools as a builder and supplementing
with Gomboc-specific best practices
"""

import os

from importlib.resources import files as ilrf


README = [
        '# {module_name}',
        'ADD TEXT',
        ]


DESCRIPTION = [
        '# pylint: disable=missing-module-docstring',
        '# pylint: disable=missing-class-docstring',
        '# pylint: disable=missing-function-docstring',
        'from importlib.resources import files as ilrf',
        # pylint: disable-next=line-too-long
        "__description__ = ilrf('{library_name}').joinpath('description.txt').read_text(encoding='UTF-8')", # noqa
        '',
        ]

INIT = [
        '# pylint: disable=missing-module-docstring',
        '# pylint: disable=missing-class-docstring',
        '# pylint: disable=missing-function-docstring',
        'from .__version__ import __version__ # noqa',
        'from .__description__ import __description__ # noqa',
        'from . import {library_name} # noqa',
        '',
        ]

VERSION = [
        '# pylint: disable=missing-module-docstring',
        '# pylint: disable=missing-class-docstring',
        '# pylint: disable=missing-function-docstring',
        '__version__ = "0.0.1"',
        '',
        ]

MAIN_HEADER = [
        '"""',
        '    main entrypoint boilerplate',
        '"""',
        'import argparse',
        '',
        'from .__version__ import __version__',
        'from .__description__ import __description__',
        'from .{library_name} import {exec_funcs}',
        '{body}',
        ]

MAIN_FUNC = [
        '',
        '',
        'def {func}_argparse():',
        '    """',
        '        argparse boilerplate code',
        '        - Add relevant options',
        '        - in case you have multiple entrypoints with different argparse',
        '          args lists, use the parent functionality from argparse',
        '          see https://docs.python.org/3/library/argparse.html',
        '    """',
        '    parser = argparse.ArgumentParser(description=__description__)',
        "    parser.add_argument('-v', '--version',",
        "                        action='version',",
        '                        version=__version__)',
        '    # add arguments here',
        '',
        '    args = parser.parse_args()',
        '    return args',
        '',
        '',
        'def {func}():',
        '    """ {func} passover """',
        '    args = {func}_argparse()',
        '    {library_name}_{func}(args)',
        '',
        ]

MAIN_CALL = [
        '',
        '',
        'def {library_name}_{func}(args):',
        '    pass',
        '',
        ]

LIBRARY = [
        'def {library_name}():',
        '    pass',
        '',
        ]


def write_file(fn, content):
    """ write a template file """
    with open(fn, 'w+', encoding='UTF-8') as f:
        f.write(content)
    f.close()


def format_content(macro, **kwargs):
    """ reformat a file list with cli args """
    return '\n'.join(macro).format(**kwargs)


class TemplateFiles:
    """ Implement creation of templated files """
    def __init__(self, module_name, library_name, exec_names):
        self.module_name = module_name
        self.library_name = library_name
        self.exec_names = exec_names
        self.process_exec()
        files = os.listdir(ilrf('pytemplate').joinpath('tpl'))
        templates_list = [f.replace('.tpl', '') for f in files]
        prefix = ilrf('pytemplate').joinpath('tpl')
        self.templates = {f.replace('DOT', '.'): prefix.joinpath(f + '.tpl')
                          for f in templates_list}

    def process_exec(self):
        """ preprocess templates entrypoint-related (if any) """
        self.library = format_content(LIBRARY, library_name=self.library_name)
        self.exec_block = ''
        self.main_content = None
        if self.exec_names is None:
            return

        self.exec_block = '\n[project.scripts]\n'
        import_funcs = []
        main_body = ''
        for word in self.exec_names:
            cli, func = word.split(':')
            self.exec_block += f"{cli} = \"{self.library_name}.__main__:{func}\"\n"
            self.library += format_content(
                    MAIN_CALL,
                    library_name=self.library_name,
                    func=func)
            import_funcs.append(self.library_name + '_' + func)
            main_body += format_content(
                    MAIN_FUNC,
                    library_name=self.library_name,
                    func=func)
        self.main_content = format_content(
                MAIN_HEADER,
                library_name=self.library_name,
                exec_funcs=', '.join(import_funcs),
                body=main_body)

    def write(self):
        """ main method to generate all from templates """
        self.write_gitignore()
        self.write_makefile()
        self.write_pylintrc()
        self.write_toml()
        self.write_tox()
        self.write_library()

    def file_copy(self, fn):
        """ simple file copy when no string changes """
        target = fn
        source = self.templates[fn]
        string = source.read_text('UTF-8')
        write_file(target, string)

    def write_gitignore(self):
        """ self explanatory """
        self.file_copy('.gitignore')

    def write_pylintrc(self):
        """ self explanatory """
        self.file_copy('pylintrc')

    def write_tox(self):
        """ self explanatory """
        self.file_copy('tox.ini')

    def write_makefile(self):
        """ self explanatory """
        fn = 'Makefile'
        target = fn
        source = self.templates[fn]
        string = source.read_text('UTF-8').format(library_name=self.library_name)
        write_file(target, string)

    def write_toml(self):
        """ self explanatory """
        fn = 'pyproject.toml'
        target = fn
        source = self.templates[fn]
        string = source.read_text('UTF-8').format(
                module_name=self.module_name,
                library_name=self.library_name,
                exec_block=self.exec_block,
                open='{',
                close='}')
        write_file(target, string)

    def write_main(self):
        """ self explanatory """
        fn = '__main__.py'
        target = os.path.join(self.library_name, fn)
        write_file(target, self.main_content)

    def write_library(self):
        """ self explanatory """
        if self.exec_names is not None:
            self.write_main()
        write_file(
                os.path.join(self.library_name, self.library_name + '.py'),
                self.library
                )


def pytemplate(args):
    """ generate a python project files structures """
    module_name = args.module[0]
    library_name = args.library[0] or module_name
    exec_names = args.exec
    descr = args.description[0]

    os.makedirs(library_name)

    TemplateFiles(module_name, library_name, exec_names).write()

    write_file('README.md', format_content(README, module_name=module_name))
    # LICENSE
    write_file(
            os.path.join(library_name, '__description__.py'),
            format_content(DESCRIPTION, library_name=library_name))
    write_file(
            os.path.join(library_name, '__init__.py'),
            format_content(INIT, library_name=library_name))
    write_file(
            os.path.join(library_name, '__version__.py'),
            format_content(VERSION))
    write_file(
            os.path.join(library_name, 'description.txt'),
            descr)
