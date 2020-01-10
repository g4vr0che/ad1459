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

from .about import AboutDialog
from .headerbar import Headerbar
from .irc_entry import IrcEntry
from .room_switcher import RoomSwitcher
from .server_popup import ServerPopover

class Ad1459Window(Gtk.Window):
    """ This is a window for AD1459. It contains the overall layout as well as
    most of the general controls for the app.
    """

    def __init__(self, app, parser):
        self.log = logging.getLogger('ad1459.window')
        self.log.debug('Creating window')

        self.app = app
        self.parser = parser

        super().__init__()
        self.set_default_size(1000, 600)

        self.about_dialog = AboutDialog()

        self.header = Headerbar(self.app)
        self.set_titlebar(self.header)

        self.main_pane = Gtk.HPaned()
        self.main_pane.set_position(200)
        self.add(self.main_pane)

        channel_grid = Gtk.Grid()
        channel_grid.set_hexpand(True)
        channel_grid.set_vexpand(True)
        self.main_pane.add2(channel_grid)

        switcher_grid = Gtk.Grid()
        switcher_grid.set_hexpand(True)
        switcher_grid.set_vexpand(True)
        self.main_pane.add1(switcher_grid)

        self.switcher = RoomSwitcher(self.app)
        switcher_grid.attach(self.switcher, 0, 0, 1, 1)

        entry_grid = Gtk.Grid()
        entry_grid.set_margin_start(6)
        entry_grid.set_margin_end(6)
        entry_grid.set_margin_top(3)
        entry_grid.set_margin_bottom(3)
        entry_grid.set_column_spacing(6)
        channel_grid.attach(entry_grid, 0, 1, 1, 1)
        
        self.irc_entry = IrcEntry(self)
        self.nick_button = Gtk.Button.new_with_label('nickname')
        self.send_button = Gtk.Button.new_from_icon_name(
            'mail-send-symbolic', Gtk.IconSize.BUTTON
        )

        self.nick_button.set_halign(Gtk.Align.START)
        self.send_button.set_halign(Gtk.Align.END)

        Gtk.StyleContext.add_class(
            self.nick_button.get_style_context(), 'flat'
        )
        Gtk.StyleContext.add_class(
            self.send_button.get_style_context(), 'suggested-action'
        )

        entry_grid.attach(self.nick_button, 0, 0, 1, 1)
        entry_grid.attach(self.irc_entry, 1, 0, 1, 1)
        entry_grid.attach(self.send_button, 2, 0, 1, 1)

        self.channel_pane = Gtk.HPaned()
        self.channel_pane.set_position(600)
        channel_grid.attach(self.channel_pane, 0, 0, 1, 1)

        self.message_stack = Gtk.Stack()
        self.message_stack.set_hexpand(True)
        self.message_stack.set_vexpand(True)
        self.message_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.message_stack.set_transition_duration(100)
        self.channel_pane.add1(self.message_stack)

        self.topic_stack = Gtk.Stack()
        self.topic_stack.set_hexpand(True)
        self.topic_stack.set_vexpand(True)
        self.topic_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.topic_stack.set_transition_duration(100)
        self.channel_pane.add2(self.topic_stack)

        self.irc_entry.grab_focus_without_selecting()
