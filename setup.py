#!/usr/bin/env python

from distutils.command.install import INSTALL_SCHEMES
from os.path import dirname, join, abspath
from setuptools import setup
from setuptools.command.install import install


for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup_args = {
    'cmdclass': {'install': install},
    'name': 'watir_snake',
    'version': "0.1.0",
    'license': 'MIT',
    'description': 'Python port of WATIR',
    'long_description': open(join(abspath(dirname(__file__)), 'README.md')).read(),
    'url': 'https://github.com/lmtierney/watir-snake',
    'classifiers': ['Intended Audience :: Developers',
                    'Operating System :: POSIX',
                    'Operating System :: Microsoft :: Windows',
                    'Operating System :: MacOS :: MacOS X',
                    'Topic :: Software Development :: Testing',
                    'Topic :: Software Development :: Libraries',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6'],
    'package_dir': {'watir_snake': 'watir_snake'},
    'packages': ['watir_snake'],
    'zip_safe': False
}

setup(**setup_args)