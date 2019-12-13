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
        self.props.selectable = False

        message_grid = Gtk.Grid()
        message_grid.props.margin = 6
        message_grid.set_hexpand(True)
        message_grid.set_column_spacing(12)
        self.add(message_grid)

        self.message_time = Gtk.Label()
        self.message_time.props.halign = Gtk.Align.END
        self.message_time.props.valign = Gtk.Align.START
        message_grid.attach(self.message_time, 0, 1, 1, 1)
        self.message_sender = Gtk.Label()
        self.message_sender.props.xalign = 1
        self.message_sender.props.halign = Gtk.Align.END
        self.message_sender.props.valign = Gtk.Align.END
        self.message_sender.props.width_request = 100
        message_grid.attach(self.message_sender, 0, 0, 1, 1)
        self.message_text = Gtk.Label()
        self.message_text.props.halign = Gtk.Align.START
        self.message_text.set_line_wrap(True)
        self.message_text.set_hexpand(True)
        self.message_text.props.xalign = 0
        message_grid.attach(self.message_text, 2, 0, 1, 2)

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
