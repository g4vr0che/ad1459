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

from .headerbar import Headerbar

class AdWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        header = Headerbar()
        self.set_titlebar(header)

        maingrid = Gtk.Grid()
        self.add(maingrid)

        content = Gtk.HPaned()
        content.set_position(300)
        content.set_hexpand(True)
        content.set_vexpand(True)
        maingrid.attach(content, 0, 0, 1, 1)

        servers_grid = Gtk.Grid()
        content.add1(servers_grid)
        servers_window = Gtk.ScrolledWindow()
        servers_grid.attach(servers_window, 0, 0, 1, 1)

        self.servers_listbox = Gtk.ListBox()
        servers_grid.attach(self.servers_listbox, 0, 0, 1, 1)

        test_message = Gtk.Grid()
        test_message.set_hexpand(True)
        test_message.props.margin = 12 
        test_message.set_column_spacing(12)
        content.add2(test_message)

        test_msg_time = Gtk.Label()
        test_msg_time.set_text('25:64')
        test_message.attach(test_msg_time, 0, 0, 1, 1)


        