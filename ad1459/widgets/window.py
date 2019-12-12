#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This file is the application window.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AdWindow(Gtk.Window):

    def __init__(self):
        super().__init__(self)
        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        