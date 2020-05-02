from distutils.core import setup
import os

description = "python script to create standard python template module"

long_description = (
)

def get_version():
    for line in open('pytemplate/__version__.py'):
        if 'version' in line:
            return line.split('=')[1].strip(' \n\'"')
    raise Error("No version")

setup(
    author="Sebastien Roy",
    author_email="sebastien.roy.sr@gmail.com",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Office/Business",
        "Topic :: Utilities"
    ],
    description=description,
    long_description=long_description,
    name='pytemplate',
    packages=['pytemplate'],
    scripts=[
            os.path.join('bin', "pytemplate"),
        ],
    version=get_version(),
    install_requires=[
        ]
)
