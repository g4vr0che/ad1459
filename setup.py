#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the Python package.
"""

from setuptools import setup, find_packages

version = {}
with open('ad1459/__version__.py') as fp:
  exec(fp.read(), version)

setup(
    name='ad1459',
    version=version['__version__'],
    packages=find_packages(),
    scripts=['ad1459/ad1459'],

    # Dependencies
    install_requires=[
      'pydle',
      'pure-sasl'
    ],

    data_files=[
      ('/usr/share/applications', ['data/in.donotspellitgav.ad1459.desktop']),
    ],

    # Project Metadata
    author='Gaven Royer',
    author_email='gavroyer@gmail.com',
    description='An IRC Client',
    keywords='ad1459 irc client chat gui gtk'
)