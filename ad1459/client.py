#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  The IRC client object.
"""

import asyncio
import logging
import pydle
import time

class Client(pydle.Client):

    def __init__(self, nick, network, sasl_username=None, sasl_password=None, **kwargs):
        self.log = logging.getLogger('ad1459.client')
        super().__init__(nick, sasl_username=sasl_username, sasl_password=sasl_password, **kwargs)
        self.network_ = network
        self.log.debug('Created client for network %s', self.network_.name)
        self.bouncer = False
    
    async def connect(self, hostname=None, password=None, **kwargs):
        self.log.debug('Client initiating connection to %s', hostname)
        await super().connect(hostname=hostname, password=password, **kwargs)
    
    async def on_connect(self):
        self.log.info('Connected to %s', self.network_.name)
        await super().on_connect()
        await self.network_.on_connected()
    
    async def on_raw(self, message):
        if message.command == ('CAP' or 'cap' or 'Cap'):
            if 'znc.in/' in " ".join(message.params):
                self.log.debug('Server appears to be a ZNC Bouncer')
                self.bouncer = True
        
        await super().on_raw(message)
    
    async def on_nick_change(self, old, new):
        self.log.debug('User %s is now %s', old, new)
        await self.network_.on_nick_change(old, new)
        await super().on_nick_change(old, new)
    
    async def on_join(self, channel, user):
        self.log.debug(f'User {user} joined {channel} on {self.network_.name}')
        await self.network_.on_join(channel, user)
        await super().on_join(channel, user)
    
    async def on_part(self, channel, user, message=None):
        self.log.debug(f'User {user} parted {channel} on {self.network_.name}')
        await self.network_.on_part(channel, user, message=message)
        await super().on_part(channel, user, message=message)
    
    async def on_quit(self, user, message=None):
        self.log.debug(f'User {user} has quit {self.network_.name}')
        await self.network_.on_quit(user, message=message)
        await super().on_quit(user, message=message)

    async def on_message(self, target, source, message):
        self.log.debug('New message in %s from %s: %s', target, source, message)
        await self.network_.on_message(target, source, message)
        await super().on_message(target, source, message)
    
    async def on_notice(self, target, by, message):
        self.log.debug('Received notice to %s from %s', target, by)
        await self.network_.on_notice(target, by, message)
        await super().on_notice(target, by, message)
    
    async def on_private_message(self, target, by, message):
        self.log.debug('New private message to %s from %s: %s', target, by, message)
        await self.network_.on_private_message(target, by, message)
        await super().on_private_message(target, by, message)
    
    async def on_private_notice(self, target, by, message):
        self.log.debug('Received private notice to %s from %s', target, by)
        await self.network_.on_private_notice(target, by, message)
        await super().on_private_notice(target, by, message)
    
    async def on_ctcp_action(self, by, target, contents):
        await self.network_.on_ctcp_action(target, by, contents)