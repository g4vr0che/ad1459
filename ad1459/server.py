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
    """ A representation of a server, with all open rooms on that server.

    Attributes:
        rooms (list of :obj:`Room`): A list containing the rooms currently in 
            use on this server.
        server_messages (:obj:`ServerRoom`): A room for this server's server 
            messages.
    """

    def __init__(self):
        self.rooms = []
        self.room = ServerRoom(self)

    @property
    def host(self):
        """str: The hostname for this connection, in the format host:port."""
        return self._host
    
    @host.setter
    def host(self, host):
        self._host = host
    
    @property
    def name(self):
        """str: The name of this server (and its room)."""
        return self.room.name
    
    @name.setter
    def name(self, name):
        """This is actually tracked by the room."""
        self.room.name = name
    
    def connect(self):
        """ Connect to the server, disconnecting first if already connected. """
        if self.host is not "test":
            pass
    
    def join_room(self, room):
        """ Join a new room/channel, or start a new private message with a user.

        Arguments:
            room (str): The name of the room/channel
        """
        new_room = Room(self)
        new_room.name = room
        self.rooms.append(new_room)
    
    def get_room_for_index(self, index):
        """ Get a room from the room list.

        Arguments:
            index (int): The index of the room to get, with 0 being the 
                server_room

        Returns:
            :obj:`Room`: The room at the given index.
        """
        return self.rooms[index]

class ServerRoom(Room):
    """ A special Room class for the server message buffer/room. """

    def __init__(self, server):
        super().__init__(server)
        self.row.kind = 'SERVER'

    def display_motd(self, motd):
        self.add_message(motd)
    
