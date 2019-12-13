#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  ListBoxRows for servers/rooms.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RoomRow(Gtk.ListBoxRow):

    def __init__(self):
        Gtk.ListBoxRow.__init__(self)

        room_grid = Gtk.Grid()
        self.add(room_grid)

        self.room_label = Gtk.Label()
        room_grid.attach(self.room_label, 0, 0, 1, 1)
    
    @property
    def room_name(self):
        return self.room_label.get_text()
    
    @room_name.setter
    def room_name(self, name):
        self.room_label.set_text(name)
        