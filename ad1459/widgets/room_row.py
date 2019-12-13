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

    def __init__(self, kind):
        Gtk.ListBoxRow.__init__(self)

        room_grid = Gtk.Grid()
        self.add(room_grid)

        self.room_label = Gtk.Label()
        room_grid.attach(self.room_label, 0, 0, 1, 1)

        self.kind = kind
    
    @property
    def room_name(self):
        return self.room_label.get_text()
    
    @room_name.setter
    def room_name(self, name):
        self.room_label.set_text(name)
    
    @property
    def kind(self):
        try:
            return self._type
        except AttributeError:
            self._type = 'room'
            return self._type
            
    @kind.setter
    def kind(self, kind):
        if kind == 'server':
            self.set_margin_top(12) 
            self.set_margin_start(0)
        elif kind == 'room': 
            self.set_margin_top(0)
            self.set_margin_start(12)
        else:
            self.set_margin_top(0)
            self.set_margin_start(18)
        self._type = kind
