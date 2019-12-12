#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the Python package.
"""

from setuptools import setup, find_packages

VERSION = '0.0.0'

setup(
    name='ad1459',
    version=VERSION,
    packages=find_packages(),
    scripts=['ad1459/ad1459'],

    # Dependencies
    install_requires=['twisted'],

    # Project Metadata
    author='Gaven Royer',
    author_email='gavroyer@gmail.com',
    description='An IRC Client',
    keywords='ad1459 irc client chat gui gtk'
)