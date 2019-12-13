#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  ListBoxRows for messages.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MessageRow(Gtk.ListBoxRow):

    def __init__(self):
        Gtk.ListBoxRow.__init__(self)

        message_grid = Gtk.Grid()
        message_grid.set_column_spacing(12)
        self.add(message_grid)

        self.message_time = Gtk.Label()
        message_grid.attach(self.message_time, 0, 0, 1, 1)
        self.message_sender = Gtk.Label()
        message_grid.attach(self.message_sender, 0, 1, 1, 1)
        self.message_text = Gtk.Label()
        message_grid.attach(self.message_text, 0, 2, 1, 1)

    @property
    def time(self):
        return self.message_time.get_text()
    
    @time.setter
    def time(self, time):
        self.message_time.set_text(time)
    
    @property
    def sender(self):
        return self.message_sender.get_text()
    
    @sender.setter
    def sender(self, sender):
        self.message_sender.set_text(sender)
    
    @property
    def text(self):
        return self.message_text.get_text()
    
    @text.setter
    def text(self, text):
        self.message_text.set_text(text)
