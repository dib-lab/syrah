from __future__ import print_function
import sys
from setuptools import setup
from setuptools import Extension
import os

VERSION="0.1"

CLASSIFIERS = [
    "Environment :: Console",
    "Environment :: MacOS X",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

#CLASSIFIERS.append("Development Status :: 5 - Production/Stable")

SETUP_METADATA = \
               {
    "name": "syrah",
    "version": VERSION,
    "description": "extract trusted k-mers from raw sequencing data",
    "url": "https://github.com/dib-lab/syrah",
    "author": "C. Titus Brown",
    "author_email": "titus@idyll.org",
    "license": "BSD 3-clause",
    "scripts": ['syrah'],
    "install_requires": ["khmer>2.0<3", "screed>=0.9<2.0"],
    "extras_require": {
        'test' : ['pytest', 'pytest-cov'],
        },
    "include_package_data": True,
    "classifiers": CLASSIFIERS
    }

setup(**SETUP_METADATA)

