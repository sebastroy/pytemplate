# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from importlib.resources import files as ilrf
__description__ = ilrf('pytemplate').joinpath('description.txt').read_text(encoding='UTF-8')
