#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Handling for networks and their rooms.
"""

import asyncio
import pydle
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from .client import Client
from .widgets.room_row import RoomRow
from .widgets.message_row import MessageRow
from .room import Room

class Network():
    """ A representation of a network, with all open rooms on that network.

    Attributes:
        rooms (list of :obj:`Room`): A list containing the rooms currently in 
            use on this network.
        network_messages (:obj:`NetworkRoom`): A room for this network's network 
            messages.
    """

    def __init__(self, app, nick, sasl_u=None, sasl_p=None):
        self.sasl_u = sasl_u
        self.sasl_p = sasl_p
        self.app = app
        self.nick = nick
        self.rooms = []
        self.room = NetworkRoom(self)
        if sasl_p:
            self.client = Client(self.nick, self, sasl_password=sasl_p, sasl_username=sasl_u)
        else:
            self.client = Client(self.nick, self)
    
    @property
    def nick(self):
        """str: the user's nickname for this network."""
        return self._nick
    
    @nick.setter
    def nick(self, nick):
        self._nick = nick

    @property
    def host(self):
        """str: The hostname for this connection"""
        return self._host
    
    @host.setter
    def host(self, host):
        self._host = host
    
    @property
    def port(self):
        """int: the port for this connection."""
        try:
            return self._port
        except AttributeError:
            return 6679
    
    @port.setter
    def port(self, port):
        self._port = port
    
    @property
    def tls(self):
        """bool: True if the connection uses TLS, otherwise False (default)."""
        try:
            return self._tls
        except AttributeError:
            return False
    
    @tls.setter
    def tls(self, tls):
        self._tls = tls
    
    @property
    def password(self):
        """str: any required password for this network."""
        try:
            return self._password
        except AttributeError:
            return ''
    
    @password.setter
    def password(self, password):
        self._password = password
    
    @property
    def auth(self):
        """str: The authentication method, none, sasl, or pass"""
        try:
            return self._auth
        except AttributeError:
            return 'none'
    @auth.setter
    def auth(self, mode):
        self._auth = mode
    
    @property
    def name(self):
        """str: The name of this network (and its room)."""
        try:
            return self.room.name
        except AttributeError:
            return self.host
    
    @name.setter
    def name(self, name):
        """This is actually tracked by the room."""
        self.room.name = name
    
    async def do_connect(self):
        """ Connect to the actual network."""
        if self.auth == 'pass':
            await self.client.connect(
                self.host,
                port=self.port,
                tls=self.tls,
                password=self.password
            )
        # elif self.auth == 'sasl':
        #     await self.client.connect(
        #         self.host,
        #         port=self.port,
        #         tls=self.tls,
        #         sasl_password=self.sasl_p,
        #         sasl_username=self.sasl_u
        #     )
        else:
            await self.client.connect(
                self.host,
                port=self.port,
                tls=self.tls
            )
        print('Connected!')
    
    def connect(self):
        """ Connect to the network, disconnecting first if already connected. """
        if self.host is not "test":
            loop = asyncio.get_event_loop()
            asyncio.run_coroutine_threadsafe(self.do_connect(), loop=loop)
    
    def join_room(self, room):
        """ Join a new room/channel, or start a new private message with a user.

        Arguments:
            room (str): The name of the room/channel
        """
        new_room = Room(self)
        new_room.name = room
        new_room.window.name = room
        self.rooms.append(new_room)
    
    def get_room_for_index(self, index):
        """ Get a room from the room list.

        Arguments:
            index (int): The index of the room to get, with 0 being the 
                network_room

        Returns:
            :obj:`Room`: The room at the given index.
        """
        return self.rooms[index]
    
    def add_message_to_room(self, channel, sender, message):
        room = self.app.window.get_active_room(room=channel)
        css = None
        skip = False
        
        if sender == (self.nick or '*'):
            messages = room.messages.get_children()
            for each in messages:
                mtext = each.message_text.get_text()
                mtime = each.message_time.get_text()
                ctime = time.ctime().split()[3]
                if (message or f'{self.nick} {message}') == mtext and ctime == mtime:
                    skip = True
        elif self.nick in message:
            css = 'highlight'
        if not skip:
            room.add_message(message, sender=sender, css=css)
            if self.app.window.get_active_room() != room:
                if self.nick in message:
                    room.row.unread_indicator.set_from_icon_name(
                        'dialog-information-symbolic',
                        Gtk.IconSize.SMALL_TOOLBAR
                    )
                else:
                    room.row.unread_indicator.set_from_icon_name(
                        'mail-unread-symbolic',
                        Gtk.IconSize.SMALL_TOOLBAR
                    )

    
    """ METHODS CALLED FROM ASYNCIO/PYDLE """

    def on_own_nick_change(self, new_nick):
        self.nick = new_nick
        GLib.idle_add(self.app.window.change_nick, new_nick)

    def on_rcvd_message(self, channel, sender, message):
        GLib.idle_add(self.add_message_to_room, channel, sender, message)
    
    def on_join_channel(self, channel):
        print(f'219: joining {channel} on {self.name}')
        GLib.idle_add(self.app.window.join_channel, channel, self.name)

class NetworkRoom(Room):
    """ A special Room class for the network message buffer/room. """

    def __init__(self, network):
        super().__init__(network)
        self.row.kind = 'SERVER'

    def display_motd(self, motd):
        self.add_message(motd)
    
