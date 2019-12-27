#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Handling for networks and their rooms.
"""

import asyncio
import logging
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

    def __init__(self, app, name, nick, sasl_u=None, sasl_p=None):
        self.log = logging.getLogger('ad1459.network')
        self.log.debug('Creating network for %s', name)
        self.sasl_u = sasl_u
        self.sasl_p = sasl_p
        self.app = app
        self.nick = nick
        self.rooms = []
        if sasl_p:
            self.client = Client(self.nick, self, sasl_password=sasl_p, sasl_username=sasl_u)
        else:
            self.client = Client(self.nick, self)
        
        self.room = NetworkRoom(self)
        self.name = name
    
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
        try:
            return self._host
        except AttributeError:
            return None
    
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
    
    def connect(self):
        """ Connect to the network, disconnecting first if already connected. """
        if self.host is not "test":
            loop = asyncio.get_event_loop()
            self.log.debug('Initiating connection')
            self.log.debug('Spinning up async connection')
            if self.auth == 'pass':
                self.log.debug('Using password authentication')
                self.log.debug('Client connection method: %s', self.client.connect)
                asyncio.run_coroutine_threadsafe(
                    self.client.connect(
                        self.host,
                        port=self.port,
                        tls=self.tls,
                        password=self.password
                    ),
                    loop=loop
                )
            else:
                self.log.debug('Using SASL authentication (or none)')
                asyncio.run_coroutine_threadsafe(
                    self.client.connect(
                        self.host,
                        port=self.port,
                        tls=self.tls
                    ),
                    loop=loop
                )
    
    def join_room(self, room, kind='channel'):
        """ Join a new room/channel, or start a new private message with a user.

        Arguments:
            room (str): The name of the room/channel
        """
        new_room = Room(self)
        new_room.name = room
        new_room.row.kind = kind
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
    
    def add_message_to_room(self, channel, sender, message, css=None):
        self.log.debug('Adding %s from %s to %s', message, sender, channel)
        room = self.app.window.get_active_room(room=channel)
        
        if self.nick in message:
            css = 'highlight'
        if sender == (self.nick):
            css = 'mine'
        elif sender == '*':
            css = 'server'

        if css:
            self.log.debug('Message has class: .%s', css)
        print(message)
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

    def join_part_user_to_room(self, channel, user, action='join'):
        room = self.app.window.get_active_room(room=channel)
        if action == 'join':
            room.tab_complete.append(user)
        elif action == 'part':
            room.tab_complete.remove(user)
        jp_message = f'{user} has {action}ed {channel}'
        self.add_message_to_room(channel, '*', jp_message, css='server')
    
    def remove_room_from_list(self, room):
        room = self.app.window.get_active_room(room=room)
        room.messages.destroy()
        room.view.destroy()
        room.window.destroy()
        room.row.destroy()
        del room

    def post_private_message(self, to, sender, message, css=None):
        """ Put a private message into the buffer.
       
        Arguments:
            to (str): the user the message was sent to.
            sender (str): the user the message was sent from.
            message (str): The message text
        """
        self.log.debug('Posting private message from %s', sender)
        if sender != self.nick:
            try:
                self.add_message_to_room(sender, sender, message, css=css)
            except AttributeError:
                self.log.debug('Adding window for PM with %s', to)
                self.app.window.join_channel(sender, self.name, 'privmsg')
                self.add_message_to_room(sender, sender, message, css=css)
        else:
            try:
                self.add_message_to_room(to, sender, message, css=css)
            except AttributeError:
                self.log.debug('Adding window for PM with %s', to)
                self.app.window.join_channel(to, self.name, 'privmsg')
                self.add_message_to_room(to, sender, message, css=css)
    
    """ METHODS CALLED FROM ASYNCIO/PYDLE """

    def on_own_nick_change(self, new_nick):
        self.nick = new_nick
        GLib.idle_add(self.app.window.change_nick, new_nick)

    def on_rcvd_message(self, channel, sender, message, css=None):
        GLib.idle_add(self.add_message_to_room, channel, sender, message, css)
    
    def on_rcvd_private_message(self, to, sender, message, css=None):
        GLib.idle_add(self.post_private_message, to, sender, message, css)
    
    def on_join_channel(self, channel):
        GLib.idle_add(self.app.window.join_channel, channel, self.name)
    
    def on_user_join_part(self, channel, user, action='join'):
        self.log.debug('User %s has %sed %s', user, action, channel)
        GLib.idle_add(self.join_part_user_to_room, channel, user, action)
    
    def on_self_part(self, channel_name):
        self.log.debug('Confirmed %s has left %s', self.nick, channel_name)
        GLib.idle_add(self.remove_room_from_list, channel_name)


class NetworkRoom(Room):
    """ A special Room class for the network message buffer/room. """

    def __init__(self, network):
        super().__init__(network)
        self.row.kind = 'SERVER'
        self.tab_complete = []

    def display_motd(self, motd):
        self.add_message(motd)
    
