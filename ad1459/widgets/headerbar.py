#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the headerbar.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Headerbar(Gtk.HeaderBar):

    def __init__(self):
        super().__init__()

        self.set_show_close_button(True)
        self.set_title('AD1459')
        self.set_has_subtitle(False)

        btn_appmenu = Gtk.MenuButton()
        self.pack_end(btn_appmenu)
        
        appmenu = Gtk.Popover()
        