[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "{module_name}"
readme = "README.md"
requires-python = ">=3.9"
dynamic = ["version", "description"]
dependencies = [
        "argparse",
]
{exec_block}
[tool.setuptools]
include-package-data = true

[tool.setuptools.package-data]
{library_name} = ["description.txt"]

[tool.setuptools.dynamic]
version = {open}attr = "{library_name}.__version__"{close}
description = {open}file = "{library_name}/description.txt"{close}
