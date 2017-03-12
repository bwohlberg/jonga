#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from glob import glob
from setuptools import setup
import io
import os.path
from ast import parse


name = 'jonga'
# See http://stackoverflow.com/questions/2058802
with open('jonga.py') as f:
    version = parse(next(filter(
        lambda line: line.startswith('__version__'),
        f))).body[0].value.s


py_modules = ['jonga']
docdirbase  = 'share/doc/%s-%s' % (name, version)
data = [(docdirbase, glob(os.path.join("examples" ,"*.py")) +
                     glob(os.path.join("examples" ,"*.ipynb")))]


longdesc = \
"""
Jonga is a Python package that generates a directed graph representing
function calls within a block of Python code, intended for inclusion
in Sphinx package documentation.
"""

on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    print("Building on ReadTheDocs")
    install_requires = ['pygraphviz']
else:
    install_requires = ['pygraphviz']


setup(
    name             = name,
    version          = version,
    py_modules       = py_modules,
    description      = 'Jonga: Python function call graph visualization',
    long_description = longdesc,
    keywords         = ['Function call graph', 'Module documentation'],
    platforms        = 'Any',
    license          = 'GPLv2+',
    url              = 'http://bwohlberg.github.io/jonga',
    author           = 'Brendt Wohlberg',
    author_email     = 'brendt@ieee.org',
    data_files       = data,
    setup_requires   = ['pytest-runner'],
    tests_require    = ['pytest'],
    install_requires = install_requires,
    classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Utilities',
    'Topic :: Software Development :: Documentation'
    ],
    zip_safe = True
)
