#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  ListBoxRows for messages.
"""

import gi
gi.require_versions(
    {
        'Gtk': '3.0',
        'Pango': '1.0'
    }
)
from gi.repository import Gtk, GLib, Pango

from ad1459.formatting import Parser

class MessageRow(Gtk.ListBoxRow):
    """ A ListBoxRow representing a message.

    The attributes for this class are stored directly in the Gtk.Label widgets
    drawn within these rows, as this obviates the need to store extra variables
    in memory.

    Attributes:
        time (str): The time the message was sent.
        sender (str): The user/network who sent the message. "*" by default.
        text (str): The text of the message.
    """

    def __init__(self):
        Gtk.ListBoxRow.__init__(self)
        self.props.selectable = False

        Gtk.StyleContext.add_class(self.get_style_context(), "message-row")
        self.props.margin = 1

        message_grid = Gtk.Grid()
        message_grid.set_hexpand(True)
        message_grid.set_margin_left(12)
        message_grid.set_margin_right(12)
        message_grid.set_column_spacing(12)
        self.add(message_grid)

        self.message_time = Gtk.Label()
        self.message_time.set_selectable(True)
        self.message_time.set_use_markup(True)
        self.message_time.props.halign = Gtk.Align.END
        self.message_time.props.valign = Gtk.Align.START
        self.message_time.props.opacity = 0.5
        message_grid.attach(self.message_time, 0, 1, 1, 1)
        self.message_sender = Gtk.Label()
        self.message_sender.set_selectable(True)
        self.message_sender.set_use_markup(True)
        self.message_sender.props.xalign = 1
        self.message_sender.props.halign = Gtk.Align.END
        self.message_sender.props.valign = Gtk.Align.END
        self.message_sender.props.width_request = 135
        self.message_sender.props.opacity = 0.8
        message_grid.attach(self.message_sender, 0, 0, 1, 1)
        self.message_text = Gtk.Label()
        self.message_text.set_selectable(True)
        self.message_text.set_use_markup(False)
        self.message_text.props.halign = Gtk.Align.START
        self.message_text.set_line_wrap(True)
        self.message_text.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.message_text.set_hexpand(True)
        self.message_text.props.xalign = 0
        message_grid.attach(self.message_text, 2, 0, 1, 2)

        self.message_text.show()
        self.message_time.show()
        self.message_sender.show()

        self.parser = Parser()
        self.kind = 'message'
    
    @property
    def kind(self):
        """str: The type of message this is, based on who sent it and 
        its contents.
        """
        return self._kind
    
    @kind.setter
    def kind(self, kind):
        self._kind = kind
        Gtk.StyleContext.add_class(self.get_style_context(), kind)
        if kind == 'server':
            self.message_text.props.opacity = 0.7

    @property
    def time(self):
        """str: The time the message was sent."""
        return self.message_time.get_text()
    
    @time.setter
    def time(self, time):
        self.message_time.set_markup(f'<i>{time}</i>')
    
    @property
    def sender(self):
        """ The sender of the message, or * for none/network. """
        return self.message_sender.get_text()
    
    @sender.setter
    def sender(self, sender):
        self.message_sender.set_markup(sender)
    
    @property
    def text(self):
        """ The message text."""
        return self.message_text.get_text()
    
    @text.setter
    def text(self, text):
        """ We need to make some conversions depending on the type of message
        this is.
        """
        if self.kind == 'action':
            text = f'\x1D{self.sender} {text}\x1D'
            self.sender = '*'
            
        escaped_text = GLib.markup_escape_text(text, len(text.encode('utf-8')))
        formatted_text = self.parser.parse_text(escaped_text)
        linked_text = self.parser.hyperlinks(formatted_text)

        self.message_text.set_markup(linked_text)
    
    def show_all_contents(self):
        self.show_all()
