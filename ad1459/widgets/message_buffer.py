#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  A buffer full of messages.
"""

import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MessageBuffer(Gtk.ScrolledWindow):

    def __init__(self, room):
        super().__init__()
        self.room = room

        self.list_box = Gtk.ListBox()
        self.list_box.set_vexpand(True)
        self.list_box.set_hexpand(True)
        self.list_box.connect('size-allocate', self.scroll_to_bottom)

        self.adj = self.get_vadjustment()
        self.adj.connect('value-changed', self.on_window_scroll)
        self.add(self.list_box)

    def add_message_to_buffer(self, message):
        """Adds a message into the buffer."""
        self.list_box.add(message)

        # Scroll to the bottom if this is our own message.
        if message.sender == self.room.network.nickname:
            self.scroll_to_bottom(self.list_box)
    
    def on_window_scroll(self, widget, data=None):
        """value-changed signal handler for the window adjustment."""
        adj = self.get_vadjustment()
        max_value = adj.get_upper() - adj.get_page_size()

        if adj.get_value() < max_value:
            try:
                self.list_box.disconnect_by_func(self.scroll_to_bottom)
            
            except TypeError:
                pass
        
        else:
            try:
                self.list_box.disconnect_by_func(self.scroll_to_bottom)
            
            except TypeError:
                pass

            self.list_box.connect('size-allocate', self.scroll_to_bottom)

    def scroll_to_bottom(self, widget, data=None):
        """Scroll to the bottom of the buffer."""
        adj = self.get_vadjustment()
        max_value = adj.get_upper() - adj.get_page_size()
        adj.set_value(max_value)