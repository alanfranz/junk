#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()

requirements = [
    'PyYAML',
    'argh==0.25.0',
    'argcomplete',
    'attrdict',
    'humanize',
    'toposort',
]

test_requirements = [
    'pytest',
]

setup(
    name='dmt',
    version='0.9.0',
    description='DMT is Yet Another Docker Management Tool, intended for rapid development.',
    long_description=readme,
    author='Blair Strang',
    author_email='blair.strang@gmail.com',
    url='https://github.com/bls/dmt',
    scripts=[
        'bin/dmt',
    ],
    packages=[
        'dmt',
    ],
    package_dir={'dmt':
                 'dmt'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='dmt',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
