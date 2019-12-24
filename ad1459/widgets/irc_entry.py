#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Then entry for using IRC.
"""

import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class IrcEntry(Gtk.Entry):
    
    def __init__(self, parent, placeholder='Enter a message'):
        self.log = logging.getLogger('ad1459.ircentry')
        super().__init__()

        self.prematched = False
        self.parent = parent
        self.set_hexpand(True)
        self.set_placeholder_text(placeholder)
        self.props.show_emoji_icon = True
        self.props.max_width_chars = 5000

        self.connect('key-press-event', self.on_key_press_event)
    
    def on_key_press_event(self, entry, event):
        if event.keyval == Gdk.keyval_from_name('Tab'):
            # We should currently get the most recent word
            # TODO: Improve this to get the current word at the cursor
            text = self.get_text()
            text_list = text.split()
            current_word = text_list[-1]
            network = self.parent.get_active_network()
            channel = self.parent.get_active_room()
            if not self.prematched:
                channel.update_tab_complete()
                self.prematched = True
            users = channel.tab_complete
            self.log.debug('Completing word %s', current_word)
            for user in users:
                print(user)
                if user.lower().startswith(current_word.lower()):
                    if text_list.index(current_word) == 0:
                        text_list.pop(-1)
                        text_list.append(f'{user}: ')
                    else:
                        text_list.pop(-1)
                        text_list.append(f'{user} ')
                    text = " ".join(text_list)
                    self.set_text(text)
                    length = len(text)
                    self.set_position(length)
            return True
            # self.log.debug('Users: %s', nicks)
