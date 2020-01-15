#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  The topic pane contents.
"""

import logging

import gi
gi.require_versions(
    {
        'Gtk': '3.0'
    }
)
from gi.repository import Gtk, GLib

from .user_row import UserRow

class TopicPane(Gtk.Grid):
    """ The contents of the topic pane, as a GtkGrid()."""

    def __init__(self, room):
        super().__init__()
        self.room = room
        self.log = logging.getLogger('ad1459.topic')
        self.topic_expander = Gtk.Expander()
        self.topic_expander.set_label_fill(True)
        self.attach(self.topic_expander, 0, 0, 1, 1)

        # Set Expander Label
        self.exp_label = Gtk.Label()
        self.exp_label.set_line_wrap(True)
        self.exp_label.set_xalign(0)
        self.exp_label.set_margin_start(3)
        self.exp_label.set_margin_end(3)
        self.topic_expander.set_label_widget(self.exp_label)

        self.topic_label = Gtk.Label()
        self.topic_label.set_margin_start(6)
        self.topic_label.set_margin_end(6)
        self.topic_label.set_margin_top(3)
        self.topic_label.set_margin_bottom(6)
        self.topic_label.set_xalign(0)
        self.topic_label.set_line_wrap(True)
        self.topic_expander.add(self.topic_label)

        separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        separator.set_hexpand(True)
        self.attach(separator, 0, 1, 1, 1)

        user_window = Gtk.ScrolledWindow()
        user_window.set_hexpand(True)
        user_window.set_vexpand(True)
        self.attach(user_window, 0, 2, 1, 1)

        self.user_list = Gtk.ListBox()
        self.user_list.set_hexpand(True)
        self.user_list.set_vexpand(True)
        self.user_list.set_sort_func(sort_users)
        user_window.add(self.user_list)

        self.update_topic()
    
    def update_topic(self):
        """Update the channel topic."""
        self.log.debug('Updating topic for %s', self.room.name)

        try:
            topic_expander_label = '<small>Set by '
            topic_by = GLib.markup_escape_text(self.room.data['topic_by'])
            topic_expander_label += f'<i>{topic_by}</i> on '
            topic_expander_label += f'<i>{self.room.data["topic_set"]}</i>:</small>'
            topic_text = GLib.markup_escape_text(self.room.data['topic'])
            topic_text = self.room.window.parser.parse_text(topic_text)
            topic_text = self.room.window.parser.hyperlinks(topic_text)
            self.topic_expander.set_sensitive(True)
            self.topic_expander.set_expanded(True)
        
        except (KeyError, TypeError):
            topic_expander_label = "No topic set"
            topic_text = ''
            self.topic_expander.set_sensitive(False)
            self.topic_expander.set_expanded(False)

        self.exp_label.set_markup(topic_expander_label)
        self.topic_label.set_markup(f'<small>{topic_text}</small>')

    def update_users(self):
        """Updates this room's user list."""
        curr_users = self.user_list.get_children()
        
        for user in curr_users:
            GLib.idle_add(user.destroy)

        for user in self.room.users:
            new_user = UserRow(self.room)
            new_user.nick = user
            self.user_list.add(new_user)
        
        self.room.window.show_all()
        self.user_list.invalidate_sort()

def sort_users(row1, row2, *user_data):
    if row1.nick.upper() < row2.nick.upper():
        return -1
    else:
        return 1