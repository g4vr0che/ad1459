#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This file is an application window.
"""

import logging

import gi
gi.require_versions(
    {
        'Gtk': '3.0',
        'Gdk': '3.0'
    }
)
from gi.repository import Gtk, Gdk
from .room_row import room_row_sort

class RoomSwitcher(Gtk.Grid):

    def __init__(self, app):
        super().__init__()
        self.app = app

        window = Gtk.ScrolledWindow()
        window.set_hexpand(True)
        window.set_vexpand(True)
        self.attach(window, 0, 0, 1, 1)

        self.switcher = Gtk.ListBox()
        self.switcher.set_hexpand(True)
        self.switcher.set_vexpand(True)
        self.switcher.set_sort_func(room_row_sort)
        window.add(self.switcher)
    
    def add_row(self, row):
        """ Adds a row to the ListBox.

        Arguments:
            row (:obj:`RoomRow`): A Room Row to add to the listbox.
        """
        self.switcher.insert(row, 0)
    
    def remove_row(self, row):
        """ Removes a row from the ListBox.

        Arguments:
            row (:obj:`RoomRow`): The row to remove
        """
        try:
            row.destroy()

        except AttributeError:
            pass

        self.switcher.invalidate_sort()
    
    def invalidate_sort(self):
        """ proxy for self.switcher.invalidate_sort()"""
        self.switcher.invalidate_sort()
    
    def get_active_room(self):
        """Gets the currently selected Room.

        Returns:
            a :obj:`Room` for the currently selected row
        """
        room = self
        room.network = ""
        return room

