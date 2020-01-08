#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the About Dialog.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ad1459 import __version__, __license__


class AboutDialog(Gtk.AboutDialog):

    def __init__(self):
        super().__init__()

        self.set_program_name('AD1459')
        self.set_logo_icon_name('in.donotspellitgav.Ad1459')
        self.set_version(__version__.__version__)
        self.set_website('https://github.com/g4vr0che/ad1459')
        self.set_website_label('github.com/g4vr0che/ad1459')
        self.set_copyright('Copyright ©2019 Gaven Royer et al')
        self.set_license(__license__.__license__)
        self.set_wrap_license(True)
        self.set_authors(
            [
                'Gaven Royer'
            ]
        )
