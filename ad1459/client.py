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
    
    async def connect(self, hostname=None, password=None, **kwargs):
        self.log.debug('Client initiating connection to %s', hostname)
        await super().connect(hostname=hostname, password=password, **kwargs)
    
    async def on_connect(self):
        self.log.info('Connected to %s', self.network_.name)
        await super().on_connect()
    
    async def on_raw(self, message):
        await super().on_raw(message)
    
    async def on_nick_change(self, old, new):
        self.log.debug('User %s is now %s', old, new)
        if old == self.network_.nick:
            self.network_.on_own_nick_change(new)
        await super().on_nick_change(old, new)
    
    async def on_join(self, channel, user):
        self.log.debug(f'User {user} joined {channel} on {self.network_.name}')
        if user == self.network_.nick:
            self.network_.on_join_channel(channel)
        else:
            self.network_.on_user_join_part(channel, user)
        await super().on_join(channel, user)
    
    async def on_part(self, channel, user):
        self.log.debug(f'User {user} parted {channel} on {self.network_.name}')
        self.network_.on_user_join_part(channel, user, action='part')
        await super().on_part(channel, user)


    async def on_message(self, target, source, message):
        self.network_.on_rcvd_message(target, source, message)
        await super().on_message(target, source, message)
    
    async def on_ctcp_action(self, by, target, contents):
        message = f'{by} {contents}'
        self.network_.on_rcvd_message(target, '*', message)