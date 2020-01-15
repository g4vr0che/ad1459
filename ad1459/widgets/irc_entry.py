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
        self.possible_completions = []

        self.connect('key-press-event', self.on_key_press_event)
    
    def on_key_press_event(self, entry, event):
        if event.keyval == Gdk.keyval_from_name('Tab'):
            # We should currently get the most recent word
            # TODO: Improve this to get the current word at the cursor
            text = self.get_text()
            text_list = text.split()
            
            try:
                current_word = text_list.pop()
            except IndexError:
                return True

            room = self.parent.message_stack.get_visible_child().room
            complete_list = room.users
            for user in room.tab_complete:
                if user in complete_list[::-1]:
                    complete_list.remove(user)
                    complete_list.insert(0, user)

            print(room.tab_complete)
            self.log.debug('Completing word %s', current_word)
            if not self.possible_completions:
                self.log.debug('Users to complete from: %s', complete_list)
                for user in complete_list:
                    if user.lower().startswith(current_word.lower()):
                        self.possible_completions.insert(0, user)
            self.log.debug(
                'Possible completions of %s: %s', 
                current_word,
                self.possible_completions
            )
            
            try:
                completion = self.possible_completions.pop()
                self.possible_completions.insert(0, completion)

                if len(text_list) == 0:
                    completion = f'{completion}:'

                completion = f'{completion} '
                text_list.append(completion)
                text = ' '.join(text_list)
                self.set_text(text)
                length = len(text)
                self.set_position(length)
            except IndexError:
                pass
            self.grab_focus_without_selecting()
            return True
        
        self.possible_completions = []
