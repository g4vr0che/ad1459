#!/usr/bin/env python3

""" AD1459, an IRC Client

  Copyright ©2019-2020 by Gaven Royer

  Permission to use, copy, modify, and/or distribute this software for any
  purpose with or without fee is hereby granted, provided that the above
  copyright notice and this permission notice appear in all copies.

  THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH REGARD
  TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
  FITNESS. IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
  ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
  SOFTWARE.

  This is the Python package.
"""

from setuptools import setup, find_packages, Command
import subprocess

version = {}
with open('ad1459/__version__.py') as fp:
    exec(fp.read(), version)

with open('README.md') as readme:
    long_description = readme.read()

class Release(Command):
    """ Generate a release and push it to git."""
    description = "Generate a release and push it to git."

    user_options = [
        ('dry-run', None, 'Skip the actual release and do a dry run instead.'),
        ('prerelease', None, 'Release this version as a pre-release.'),
        ('force-version=', None, 'Force the version to update to the given value.')
    ]

    def initialize_options(self):
        self.dry_run = False
        self.prerelease = False
        self.force_version = None
    
    def finalize_options(self):
        if self.force_version:
            if not isinstance(self.force_version, str):
                raise Exception('Please specify the test version to release')

    def run(self):
        command = ['npx', 'standard-version@next']
        if self.dry_run:
            command.append('--dry-run')
        if self.prerelease:
            command.append('--prerelease')
        if self.force_version:
            # See https://github.com/conventional-changelog/standard-version#release-as-a-target-type-imperatively-npm-version-like
            command.append('--release-as')
            command.append(self.force_version)
        print(command)
        subprocess.run(command)
        if not self.dry_run:
            subprocess.run(
                ['git', 'push', '--follow-tags']
            )

setup(
    name='ad1459',
    version=version['__version__'],
    packages=find_packages(),
    scripts=['ad1459/ad1459'],

    # Dependencies
    install_requires=[
      'pydle',
      'pure-sasl',
      'keyring'
    ],

    data_files=[
      ('/usr/share/applications', ['data/in.donotspellitgav.ad1459.desktop']),
      ('/usr/share/icons/hicolor/scalable/apps', [
          'data/in.donotspellitgav.Ad1459.svg',
          'data/in.donotspellitgav.Ad1459.Devel.svg'
      ]),
      ('/usr/share/icons/hicolor/symbolic/apps', [
          'data/in.donotspellitgav.Ad1459-symbolic.svg'
      ])
    ],

    # Commands
    cmdclass={'release': Release},

    # Project Metadata
    author='Gaven Royer',
    author_email='gavroyer@gmail.com',
    description='An IRC Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='ad1459 irc client chat gui gtk',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Gnome",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Communications :: Chat :: Internet Relay Chat"
    ]
)