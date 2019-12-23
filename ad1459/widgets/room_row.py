#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  ListBoxRows for networks/rooms.
"""

from enum import Enum

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class RoomKind(Enum):
    """ An enum to classify the type of room this is.
    """
    SERVER = 1
    CHANNEL = 2
    ROOM = 2
    PRIVMSG = 3
    QUERY = 3
    DIALOG = 3
    WHISPER = 3

    def __str__(self):
        """ Turn this back into a string. """
        strings = {
            1: 'network',
            2: 'channel',
            3: 'user'
        }
        return strings[self.value]

class RoomRow(Gtk.ListBoxRow):
    """ A dedicated ListBoxRow for representing a room in the Room List.

    Arguments:
        kind (:obj:`RoomKind`): The type of room this is.
    
    Attributes:
        room_name (str): The name of this room.
        kind (RoomKind Enum): The type of room this is.
    """

    def __init__(self, room, network, kind='CHANNEL'):
        Gtk.ListBoxRow.__init__(self)
        self.network = network

        room_grid = Gtk.Grid()
        room_grid.set_column_spacing(6)
        self.add(room_grid)

        self.room_label = Gtk.Label()
        room_grid.attach(self.room_label, 0, 0, 1, 1)
        
        self.unread_indicator = Gtk.Image.new_from_icon_name(
            'mail-read-symbolic',
            Gtk.IconSize.SMALL_TOOLBAR
        )
        room_grid.attach(self.unread_indicator, 1, 0, 1, 1)

        self.kind = kind
        self.room = room
    
    @property
    def room_name(self):
        """str: The name of this room in the room list."""
        return self.room_label.get_text()
    
    @room_name.setter
    def room_name(self, name):
        """ We just store this in the label for the room."""
        self.room_label.set_text(name)
    
    @property
    def kind(self, str=False):
        """ RoomKind Enum: The type of room this is. """
        if str:
            return str(self._type)
        else:
            return self._type

            
    @kind.setter
    def kind(self, kind):
        """ We need to set some GTK Styling prefs when this is set. """
        self._type = RoomKind[kind.upper()]

        if self._type is RoomKind.SERVER:
            self.set_margin_top(12) 
            self.set_margin_start(0)
        elif self._type == RoomKind.CHANNEL: 
            self.set_margin_top(0)
            self.set_margin_start(12)
        else:
            self.set_margin_top(0)
            self.set_margin_start(18)
