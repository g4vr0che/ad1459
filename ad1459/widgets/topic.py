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

        self.update_topic()
    
    def update_topic(self):
        """Update the channel topic."""
        self.log.debug('Updating topic for %s', self.room.name)

        try:
            self.log.debug('Raw topic: %s', self.room.data['topic'])
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

        self.log.debug('%s topic set to %s', self.room.name, topic_text)
        self.exp_label.set_markup(topic_expander_label)
        self.topic_label.set_markup(topic_text)
