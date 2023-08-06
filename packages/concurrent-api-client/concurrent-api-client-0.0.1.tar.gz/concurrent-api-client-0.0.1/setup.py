#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def get_readme():
    """ Get the README from the current directory. If there isn't one, return an empty string """
    all_readmes = sorted(glob("README*"))
    if len(all_readmes) > 1:
        warnings.warn("There seems to be more than one README in this directory. Choosing the "
                      "first in lexicographic order.")
    if len(all_readmes) > 0:
        return open(all_readmes[0], 'r').read()

    warnings.warn("There doesn't seem to be a README in this directory.")
    return ""

def parse_requirements(filename):
    """ Given a filename, strip empty lines and those beginning with # """
    output = []
    with open(filename, 'r') as f:
        for line in f:
            sline = line.strip()
            if sline and not line.startswith('#'):
                output.append(sline)
    return output

def find_modules():
    found = []
    for pattern in ['src/*.py']:
#    for pattern in ['src/*.py', 'src/*.json']:
        found.extend([splitext(basename(path))[0] for path in glob(pattern)])
    return found

setup(
    name='concurrent-api-client',
    version='0.0.1',
    license='MIT',
    description='An example for API client using python request library',
    long_description="\n" + get_readme(),
    author='tatoflam',
    author_email='tatoflam@gamil.com',
    url='https://github.com/tatoflam/concurrent-api-client',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=find_modules(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    project_urls={
#        'Changelog': 'https://github.com/tatoflam/concurrent-api-client/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/tatoflam/concurrent-api-client/issues',
    },
    keywords=[
        'request', 'API', 'REST', 'client', 'async', 'concurrent'
    ],
    python_requires='>=3.7',
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("requirements.testing.txt"),
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'pytest-runner', # this could cause ERROR: No matching distribution found for pytest-runner
    ],
    entry_points={
        # 'console_scripts': [
        #     'nameless = nameless.cli:main',
        # ]
    },
)