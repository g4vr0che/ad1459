#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Handling for rooms.
"""

import asyncio
import enum
import logging
import time as Time

from .widgets.message_buffer import MessageBuffer
from .widgets.message_row import MessageRow
from .widgets.room_row import RoomRow, RoomKind
from .widgets.topic import TopicPane

class Room:
    """ A Room object that represents a list of grouped messages on IRC. This 
    can be a channel, PM conversation/dialog/query, or a list of 
    server messages.
    
    Attributes:
        buffer (:obj:): The message buffer for this room.
        topic (:obj:): The room topic (if applicable).
        row (:obj:`RoomRow`) The row for this room in the switcher.
    """

    def __init__(self, app, network, window, name):
        self.log = logging.getLogger('ad1459.room')
        self.log.debug('Creating new room %s', name)

        self.app = app
        self.network = network 
        self.window = window

        self.name = name

        self.buffer = MessageBuffer(self)
        self.row = RoomRow(self)
        self.topic_pane = TopicPane(self)
    
    # Methods
    def add_message(self, message, sender='*', time=None, kind='message'):
        """ Adds a message into this room and inserts it into the buffer.

        Arguments:
            message (str): the text of the message to add.
            sender (str): The person/entity who sent the message
            time (str): The time the message was sent.
            kind (str): The type of message this is (default: 'message')
        """
        if not time:
            time = Time.ctime().split()[3]
        new_message = MessageRow()
        new_message.kind = kind
        new_message.time = time
        new_message.sender = sender
        new_message.text = message

        self.buffer.add_message_to_buffer(new_message)

    # Data
    @property
    def data(self):
        """dict: A dictionary with this channel's data."""
        return self.network.client.channels[self.name]

    @property
    def kind(self):
        """:obj:`RoomKind` The type of room this is."""
        return self._kind
    
    @kind.setter
    def kind(self, kind):
        self.log.debug('Setting room type for %s to %s', self.name, kind)
        kind = kind.upper()
        self._kind = RoomKind[kind]
        self.row.set_margins()
        self.log.debug('Set margins for %s room', kind)

    @property
    def name(self):
        """str: The name of this channel. This is displayed in the UI, and is
        the name of the channel, the network, or the user we are chatting with.
        """
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def id(self):
        """str: The internal ID of this channel. This is used internally to 
        identify this room and it's children within the UI.

        We use the id() function to get a unique identifier for self, since this
        is guaranteed to be unique while the object exists.
        """
        return f'{self.name}-{id(self)}'
