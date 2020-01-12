#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  ListBoxRows for networks/rooms.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class UserRow(Gtk.ListBoxRow):

    def __init__(self, room):
        super().__init__()
        self.room = room
        grid = Gtk.Grid()
        grid.set_column_spacing(6)
        grid.set_margin_top(3)
        grid.set_margin_bottom(3)
        grid.set_margin_start(3)
        grid.set_margin_end(3)
        self.add(grid)

        self.status_image = Gtk.Image.new_from_icon_name(
            'radio-symbolic',
            Gtk.IconSize.SMALL_TOOLBAR
        )
        self.status_image.props.opacity = 0
        grid.attach(self.status_image, 0, 0, 1, 1)

        self.user_label = Gtk.Label()
        grid.attach(self.user_label, 1, 0, 1, 1)
    
    # Data
    @property
    def nick(self):
        """str: The user's nickname."""
        return self.user_label.get_text()
    
    @nick.setter
    def nick(self, nick):
        self.user_label.set_text(nick)

        