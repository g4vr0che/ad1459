#!/usr/bin/env python3

""" AD1459, an IRC Client

  Copyright ©2019-2020 by Gaven Royer

  Permission to use, copy, modify, and/or distribute this software for any
  purpose with or without fee is hereby granted, provided that the above
  copyright notice and this permission notice appear in all copies.

  THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH REGARD
  TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
  FITNESS. IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
  ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
  SOFTWARE.

  Then entry for using IRC.
"""

import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class IrcEntry(Gtk.Entry):
    """ An entry specifically tailored to entering IRC messages. 
    
    Includes tab-complete features.
    """

    
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
