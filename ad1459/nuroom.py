#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Handling for rooms.
"""

import asyncio
import logging

class Room:
    """ A Room object that represents a list of grouped messages on IRC. This 
    can be a channel, PM conversation/dialog/query, or a list of 
    server messages.
    
    Attributes:
        buffer (:obj:): The message buffer for this room.
        topic (:obj:): The room topic (if applicable).
        row (:obj:`RoomRow`) The row for this room in the switcher.
    """

    def __init__(self, app, network, window):
        self.app = app
        self.network = network 
        self.window = window

        self.buffer = "insert buffer here"
        self.row = "insert row here"
        self.topic = 'insert topic here'
