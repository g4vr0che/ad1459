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

  ListBoxRows for networks/rooms.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class UserRow(Gtk.ListBoxRow):
    """ A row for a user in the user list.

    The attributes for this class are stored in the label widget for this row.

    Attributes:
        nick (str): This user's nickname.
    """

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

        