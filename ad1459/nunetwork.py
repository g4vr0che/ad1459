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

    def __init__(self, app):
        self.log = logging.getLogger('ad1459.network')
        self.log.debug('Creating network')
        self.app = app
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
        loop = asyncio.get_event_loop()

        self.log.debug('Spinning up async connection to %s', self.host)
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
    
    # Data for this object.
    @property
    def name(self):
        """str: The name of this network (and its room)."""
        return self._config['name']
    
    @name.setter
    def name(self, name):
        """This is actually tracked by the room."""
        self._config['name'] = name
    
    @property
    def auth(self):
        """str: One of 'sasl', 'pass', or 'none'."""
        return self._config['auth']
    
    @auth.setter
    def auth(self, auth):
        """Only set if it's a valid value."""
        print(auth)
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
        self._config['nickname'] = nickname

    @property
    def username(self):
        """str: The username to use for the connection"""
        return self._config['username']
    
    @username.setter
    def username(self, username):
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
        self._config['password'] = password
