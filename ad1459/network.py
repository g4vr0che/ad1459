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

from .widgets.room_row import RoomRow
from .widgets.message_row import MessageRow
from .client import Client
from .formatting import Parser
from .room import Room

class Network():
    """ A representation of a network, with all open rooms on that network.

    Attributes:
        rooms (list of :obj:`Room`): A list containing the rooms currently in 
            use on this network.
        network_messages (:obj:`NetworkRoom`): A room for this network's network 
            messages.
    """

    def __init__(self, app):
        self.log = logging.getLogger('ad1459.network')
        self.log.debug('Creating network')
        self.app = app
        self.rooms = []
        self.config = {
            'name': 'New Network',
            'auth': 'sasl',
            'host': 'chat.freenode.net',
            'port': 6697,
            'tls': True,
            'nickname': 'ad1459-user',
            'username': 'ad1459-user',
            'realname': 'AD1459 User',
            'password': 'hunter2'
        }
        self.parser = Parser()
        self.room = NetworkRoom(self)

    @property
    def name(self):
        """str: The name of this network (and its room)."""
        return self.config['name']
    
    @name.setter
    def name(self, name):
        """This is actually tracked by the room."""
        self.config['name'] = name
    
    @property
    def auth(self):
        """str: One of 'sasl', 'pass', or 'none'."""
        return self.config['auth']
    
    @auth.setter
    def auth(self, auth):
        """Only set if it's a valid value."""
        print(auth)
        if auth == 'sasl' or auth == 'pass' or auth == 'none':
            self.config['auth'] = auth

    @property
    def host(self):
        """str: The hostname of the server to connect to."""
        return self.config['host']
    
    @host.setter
    def host(self, host):
        self.config['host'] = host
    
    @property
    def port(self):
        return self.config['port']
    
    @port.setter
    def port(self, port):
        """ Only set a port that is within the valid range."""
        if port > 0 and port <= 65535:
            self.config['port'] = int(port)

    @property
    def tls(self):
        """bool: Whether or not to use TLS"""
        return self.config['tls']
    
    @tls.setter
    def tls(self, tls):
        self.config['tls'] = tls

    @property
    def nickname(self):
        """str: The user's nickname"""
        return self.config['nickname']
    
    @nickname.setter
    def nickname(self, nickname):
        self.config['nickname'] = nickname

    @property
    def username(self):
        """str: The username to use for the connection"""
        return self.config['username']
    
    @username.setter
    def username(self, username):
        self.config['username'] = username

    @property
    def realname(self):
        """str: The user's real name"""
        return self.config['realname']
    
    @realname.setter
    def realname(self, realname):
        self.config['realname'] = realname

    @property
    def password(self):
        """str: The user's password."""
        return self.config['password']
    
    @password.setter
    def password(self, password):
        self.config['password'] = password
    
    
    def connect(self):
        """ Connect to the network, disconnecting first if already connected. """
        if self.auth == 'sasl':
            self.client = Client(self.nickname, self, sasl_password=self.password, sasl_username=self.username)
        else:
            self.client = Client(self.nickname, self)
        if self.host != "test":
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
            
            self.app.window.network_popover.reset_all_text()
    
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
        new_room.update_tab_complete()
    
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

        int_name = f'{id(self)}-{channel}'
        self.log.debug('Looking for internal name %s', int_name)

        room = self.app.window.get_active_room(room=int_name)
        self.log.debug('Got room %s', room.internal_name)
        
        if self.nickname in message:
            css = 'highlight'
        if sender == (self.nickname):
            css = 'mine'
        elif sender == '*':
            css = 'server'

        if css:
            self.log.debug('Message has class: .%s', css)
        room.add_message(message, sender=sender, css=css)
        if self.app.window.get_active_room() != room:
            if self.nickname in message:
                room.row.unread_indicator.set_from_icon_name(
                    'dialog-information-symbolic',
                    Gtk.IconSize.SMALL_TOOLBAR
                )
            elif room.row.icon != 'dialog-information-symbolic':
                room.row.unread_indicator.set_from_icon_name(
                    'mail-unread-symbolic',
                    Gtk.IconSize.SMALL_TOOLBAR
                )
        if not self.app.window.props.is_active:
            if self.nickname in message:
                subject = f'{sender} mentioned you in {room.name}!'
                clean_message = self.parser.sanitize_message(message)
                room.notification.update(subject, clean_message)
                room.notification.show()

    def join_part_user_to_room(self, channel, user, action='join'):
        channel_internal = f'{channel}-{self.host}-{self.nickname}'
        self.log.debug('Looking for internal name %s', channel_internal)
        
        int_name = f'{id(self)}-{channel}'
        self.log.debug('Looking for internal name %s', int_name)

        room = self.app.window.get_active_room(room=int_name)
        self.log.debug('Got room %s', room.internal_name)

        if action == 'join':
            room.tab_complete.append(user)
            action = 'joined'
        elif action == 'part':
            room.tab_complete.remove(user)
            action = 'left'
        elif action == 'quit':
            room.tab_complete.remove(user)
            action = 'quit'
        jp_message = f'{user} has {action} {channel}'
        self.add_message_to_room(channel, '*', jp_message, css='server')
    
    def quit_user(self, user, message=None):
        for room in self.rooms:
            if user in room.tab_complete:
                room.tab_complete.remove(user)
                jp_message = f'{user} has quit. ({message})'
                self.add_message_to_room(room.name, '*', jp_message, css='server')
    
    def change_user_nick(self, old, new):
        for room in self.rooms:
            if old in room.tab_complete:
                room.tab_complete.append(new)
                room.tab_complete.remove(old)
                cn_message = f'{old} is now {new}'
                self.add_message_to_room(room.name, '*', cn_message, css='server')

    
    def remove_room_from_list(self, room):
        room_internal = f'{room}-{self.host}-{self.nickname}'
        self.log.debug('Looking for internal name %s', room_internal)
        
        int_name = f'{id(self)}-{room}'
        self.log.debug('Looking for internal name %s', int_name)

        room = self.app.window.get_active_room(room=int_name)
        self.log.debug('Got room %s', room.internal_name)

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
        if sender != self.nickname:
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
        self.nickname = new_nick
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
    
    def on_user_quit(self, user, message=None):
        self.log.debug('User %s has quit %s', user, self.name)
        GLib.idle_add(self.quit_user, user, message)
        
    def on_self_part(self, channel_name):
        self.log.debug('Confirmed %s has left %s', self.nickname, channel_name)
        GLib.idle_add(self.remove_room_from_list, channel_name)
    
    def on_user_nick_change(self, old, new):
        self.log.debug('User %s has changed nicks', old)
        GLib.idle_add(self.change_user_nick, old, new)


class NetworkRoom(Room):
    """ A special Room class for the network message buffer/room. """

    def __init__(self, network):
        super().__init__(network)
        self.row.kind = 'SERVER'
        self.tab_complete = []
        self.name = self.network.name

    def display_motd(self, motd):
        self.add_message(motd)
    
