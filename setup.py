#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pubfind setup."""
from __future__ import unicode_literals

from setuptools import setup

name = str('pubpdf')

dependencies = [
    'bibutils',
    'citeproc-py',
    'ConfigArgParse',
    'lxml',
    'pyoai',
    'requests',
    'weasyprint',
]

dependency_links = [
    'git+https://github.com/jayvdb/citeproc-py@ap-2016-cherries#egg=citeproc-py',
]

setup(
    name=name,
    version='0.1.0',
    description='Publication to PDF command line tool.',
    keywords='csl fedora json schema publication article journal pdf',
    author='John Vandenberg',
    author_email='jayvdb@gmail.com',
    url='https://github.com/jayvdb/pubpdf',
    license='MIT',
    packages=[name],
    install_requires=dependencies,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [name + ' = ' + name + '.cmd:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
