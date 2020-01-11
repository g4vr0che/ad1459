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
from .commands import Commands
from .formatting import Parser
from .nuroom import Room

class Network:
    """An IRC network to connect to and chat on.

    Attributes:
        rooms (list of :obj:`Room`): A list of the joined rooms on this network.
        name (str): The user-defined name for this network.
        auth (str): The user-authentication for this network. 'sasl', 'pass', 
            or 'none'.
        host (str): The hostname for the server to connect to.
        port (int): The port number to use.
        tls (bool): Wheter the connection uses TLS encryption.
        nickname (str): The user's nickname on this network.
        realname (str): The user's Real Name on this network.
        password (str): The authentication for the password on this network.
        app (:obj:`Ad1459Application`): The app we're running on.
    """
    cmd = Commands()
    commands = {
        '/me': cmd.me
    }

    def __init__(self, app, window):
        self.log = logging.getLogger('ad1459.nunetwork')
        self.log.debug('Creating network')
        self.app = app
        self.window = window
        self.rooms = []
        self._config = {
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
        self.client = None

    # Synchronous Methods for this object.
    def connect(self):
        """ Connect to the network, disconnecting first if already connected. """
        if self.auth == 'sasl':
            self.client = Client(
                self.nickname, 
                self, 
                sasl_password=self.password, 
                sasl_username=self.username
            )
        else:
            self.client = Client(self.nickname, self)
        
        self.client.username = self.username

        self.log.debug('Spinning up async connection to %s', self.host)

        self.server_room = Room(self.app, self, self.window, self.name)
        self.server_room.kind = "server"
        self.add_room(self.server_room)

        if self.auth == 'pass':
            self.log.debug('Using password authentication')
            asyncio.run_coroutine_threadsafe(
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    tls=self.tls,
                    password=self.password
                ),
                loop=asyncio.get_event_loop()
            )

        else:
            self.log.debug('Using SASL authentication (or none)')
            asyncio.run_coroutine_threadsafe(
                self.client.connect(
                    hostname=self.host,
                    port=self.port,
                    tls=self.tls
                ),
                loop=asyncio.get_event_loop()
            )
    
    def join_channel(self, channel):
        """ Joins a room on the network."""
        asyncio.run_coroutine_threadsafe(
            self.client.join(channel), loop=asyncio.get_event_loop()
        )

    def add_room(self, room):
        """Adds a room to the window for this network."""
        self.log.debug('Adding room %s to the window', room.name)
        self.window.switcher.add_row(room.row)
        self.window.message_stack.add_named(room.buffer, room.id)
        self.window.topic_stack.add_named(room.topic_pane, room.id)
        self.window.show_all()
        self.window.switcher.switcher.invalidate_sort()
        self.rooms.append(room)
    
    def get_room_for_name(self, name):
        """ Gets a room object given the name."""
        for room in self.rooms:
            if room.name == name:
                return room

        if not name.startswith('#'):
            new_room = Room(self.app, self, self.window, name)
            new_room.kind='query'
            self.add_room(new_room)
            return new_room
    
    def send_message(self, room, message):
        """ Sends a message to the entity for room."""
        for command in self.commands:
            if not message.startswith(command):
                asyncio.run_coroutine_threadsafe(
                    self.client.message(room.name, message),
                    loop=asyncio.get_event_loop()
                )
            else:
                self.commands[command](room, self.client, message)

    
    # Asynchronous Callbacks
    async def on_connected(self):
        """ Called upon connection to IRC."""
        self.log.info('Connected to %s', self.name)
        GLib.idle_add(self.do_connected)
    
    def do_connected(self):
        popup = self.window.header.server_popup
        popup.reset_all_text()
        popup.layout_grid.set_sensitive(True)
        popup.popdown()
        self.window.switcher.switcher.invalidate_sort()
    
    async def on_nick_change(self, old, new):
        self.log.debug('Nick %s changed to %s', old, new)
        GLib.idle_add(self.do_nick_change, old, new)
    
    def do_nick_change(self, old, new):
        if old == self.nickname:
            self.nickname = new
        
        for room in self.rooms:
            if old in room.users or new in room.users:
                room.update_users()
    
    async def on_join(self, channel, user):
        self.log.debug('%s has joined %s', user, channel)
        GLib.idle_add(self.do_join, channel, user)
    
    def do_join(self, channel, user):
        if user == self.nickname:
            new_channel = Room(self.app, self, self.window, channel)
            new_channel.kind = 'channel'
            new_channel.name = channel
            new_channel.topic_pane.update_topic()
            self.add_room(new_channel)
        
        room = self.get_room_for_name(channel)
        room.add_message(f'{user} has joined', kind='server')
        self.window.show_all()
        room.topic_pane.update_users()
    
    async def on_part(self, channel, user, message=None):
        self.log.debug('%s has left %s, (%s)', user, channel, message)
        GLib.idle_add(self.do_part, channel, user, message)
    
    def do_part(self, channel, user, message=None):
        room = self.get_room_for_name(channel)
        if user == self.nickname:
            room.leave()
            self.rooms.remove(room)
            self.window.switcher.switcher.invalidate_sort()
        
        else:
            room.topic_pane.update_users()
            room.add_message(f'{user} has left ({message})', kind='server')
            self.window.show_all()
    
    async def on_quit(self, user, message=None):
        self.log.debug('%s has quit! (%s)', user, message)
        GLib.idle_add(self.do_quit, user, message)
    
    def do_quit(self, user, message=None):
        qmessage = f'{user} has quit. ({message})'
        for room in self.rooms:
            if user in room.users:
                room.add_message(qmessage, kind='server')
                room.topic_pane.update_users()
    
    async def on_message(self, target, source, message):
        self.log.debug('%s messaged to %s: %s', source, target, message)
        GLib.idle_add(self.do_message, target, source, message)
    
    def do_message(self, target, source, message):
        if target.startswith('#'):
            room = self.get_room_for_name(target)
            self.log.debug('Adding message to %s', room.id)
            room.add_message(message, source)
            room.update_tab_complete(source)
            self.window.show_all()

    async def on_notice(self, target, source, message):
        self.log.debug('%s noticed to %s: %s', source, target, message)
        GLib.idle_add(self.on_notice, target, source, message)
    
    def do_notice(self, target, source, message):
        room = self.get_room_for_name(target)
        self.log.debug('Adding notice to %s', room.id)
        room.add_message(message, source, kind='notice')
        room.update_tab_complete(source)
        self.window.show_all()
    
    async def on_private_message(self, target, source, message):
        self.log.debug('PM to %s from %s: %s', target, source, message)
        GLib.idle_add(self.do_private_message, target, source, message)

    def do_private_message(self, target, source, message):
        if target == self.nickname:
            room = self.get_room_for_name(source)
            self.log.debug('Adding message from %s', room.id)
        else:
            room = self.get_room_for_name(target)
            self.log.debug('Adding message to %s', room.id)
        
        room.add_message(message, source)
        self.window.show_all()
    
    async def on_private_notice(self, target, source, message):
        self.log.debug('Private Notice to %s from %s: %s', target, source, message)
        GLib.idle_add(self.do_private_notice, target, source, message)
        
    def do_private_notice(self, target, source, message):
        room = self.get_room_for_name(source)
        self.log.debug('Adding notice from %s', room.id)
        room.add_message(message, source, kind='notice')
        self.window.show_all()
    
    async def on_ctcp_action(self, target, source, action):
        self.log.debug('Action in %s from %s: %s %s', target, source, source, action )
        GLib.idle_add(self.do_ctcp_action, target, source, action)
        
    def do_ctcp_action(self, target, source, action):
        self.log.debug('Adding action from %s to %s', source, target)
        if target.startswith('#'):
            room = self.get_room_for_name(target)
        elif target == self.nickname:
            room = self.get_room_for_name(source)
        
        message = f'{source} {action}'
        room.add_message(message, kind='action')
        self.window.show_all()
        room.update_tab_complete(source)

    # Data for this object.
    @property
    def name(self):
        """str: The name of this network (and its room)."""
        return self._config['name']
    
    @name.setter
    def name(self, name):
        """This is actually tracked by the room."""
        self.log.debug('Setting name to %s', name)
        self._config['name'] = name
    
    @property
    def auth(self):
        """str: One of 'sasl', 'pass', or 'none'."""
        return self._config['auth']
    
    @auth.setter
    def auth(self, auth):
        """Only set if it's a valid value."""
        if auth == 'sasl' or auth == 'pass' or auth == 'none':
            self._config['auth'] = auth

    @property
    def host(self):
        """str: The hostname of the server to connect to."""
        return self._config['host']
    
    @host.setter
    def host(self, host):
        self._config['host'] = host
    
    @property
    def port(self):
        return self._config['port']
    
    @port.setter
    def port(self, port):
        """ Only set a port that is within the valid range."""
        if port > 0 and port <= 65535:
            self._config['port'] = int(port)

    @property
    def tls(self):
        """bool: Whether or not to use TLS"""
        return self._config['tls']
    
    @tls.setter
    def tls(self, tls):
        self._config['tls'] = tls

    @property
    def nickname(self):
        """str: The user's nickname"""
        return self._config['nickname']
    
    @nickname.setter
    def nickname(self, nickname):
        self.log.debug('Setting nickname to %s', nickname)
        self._config['nickname'] = nickname

    @property
    def username(self):
        """str: The username to use for the connection"""
        return self._config['username']
    
    @username.setter
    def username(self, username):
        self.log.debug('Setting username to %s', username)
        self._config['username'] = username

    @property
    def realname(self):
        """str: The user's real name"""
        return self._config['realname']
    
    @realname.setter
    def realname(self, realname):
        self._config['realname'] = realname

    @property
    def password(self):
        """str: The user's password."""
        return self._config['password']
    
    @password.setter
    def password(self, password):
        self.log.debug('Setting password')
        self._config['password'] = password
