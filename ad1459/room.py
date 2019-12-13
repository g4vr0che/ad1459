#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Handling for rooms and their messages.
"""

import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .widgets.message_row import MessageRow
from .widgets.room_row import RoomRow

class Room():

    def __init__(self):
        self.messages = Gtk.ListBox()
        self.row = RoomRow('room', self)
        self.add_message('jeans has joined')
        # self.populate_test_data()
    
    @property
    def name(self):
        return self.row.room_name
    
    @name.setter
    def name(self, name):
        self.row.room_name = name

    def get_messages(self):
        return self.messages
    
    def add_message(self, message, sender=None, msg_time=None):
        new_message = MessageRow()

        if msg_time:
            new_message.time = msg_time
        else:
            new_message.time = time.ctime().split()[3]
        
        new_message.sender = '*'
        if sender:
            new_message.sender = sender
        
        new_message.text = message

        self.messages.add(new_message)

    def populate_test_data(self):
        
        self.add_message('jeans has joined')
        self.add_message('Hi', sender='jeans')
        self.add_message('hoi', sender='gav')
        self.add_message('How are things', sender='notgav')
        self.add_message('Okay', sender='gav')
        self.add_message(
            (
                'Now it\'s even longer and it will run off the edge of the '
                'boundary so that I can see what it will look like really long. '
                'This is a really long message that I want to send because I '
                'want to see what it looks like in-context. Now it\'s going to '
                'be really long, yay!'
            ), 
            sender='jeans'
        )
        self.add_message('wow spam', sender='gav')
        self.add_message('rood', sender='notgav')
        self.add_message('sorry', sender='jeans')
        self.add_message('bye', sender='gav')
        self.add_message('\\o', sender='notgav')
