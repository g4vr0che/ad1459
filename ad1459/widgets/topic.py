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

class TopicPane(Gtk.Grid):
    """ The contents of the topic pane, as a GtkGrid()."""

    def __init__(self, room):
        self.topic_expander = Gtk.Expander()
        self.topic_expander.set_expanded(True)
        self.topic_expander.set_label_fill(True)
        self.topic_expander.set_use_markup(True)
        self.attach(self.topic_expander)

        self.topic_label = Gtk.Label()
        self.topic_expander.add(self.topic_label)

        self.update_topic()
    
    def update_topic(self):
        """Update the channel topic."""
        try:
            topic_expander_label = 'Set by '
            topic_by = GLib.markup_escape_text(self.room.data['topic_by'])
            topic_expander_label += f'<i>{topic_by}</i> on '
            topic_expander_label += f'<i>{self.room.data["topic_set"]}</i>:'
            topic_text = GLib.markup_escape_text(self.room.data['topic'])
            topic_text = self.app.parser.parse_text(topic_text)
            topic_text = self.app.parser.hyperlinks(topic_text)
        
        except AttributeError:
            topic_expander_label = "No topic set"
            topic_text = ''
            self.topic_expander.set_sensitive(False)

        self.topic_expander.set_label(topic_expander_label)
        self.topic_label.set_markup(topic_text)
