#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Handling for servers and their rooms.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .widgets.room_row import RoomRow
from .widgets.message_row import MessageRow
from .room import Room

class Server():

    def __init__(self):
        self.rooms = []
        self.server_messages = ServerRoom()

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self, host):
        self._host = host
    
    def connect(self):
        if self.host is not "test":
            pass
    
    def join_room(self, room):
        new_room = Room()
        new_room_index = len(self.rooms) + 2
        self.rooms.append((new_room_index, new_room))
    
    def get_room_for_index(self, index):
        return self.rooms[index]

class ServerRoom(Room):

    def display_motd(self, motd):
        self.add_message(motd)
    