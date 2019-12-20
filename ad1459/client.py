#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  The IRC client object.
"""

import asyncio
import pydle
import time

class Client(pydle.Client):

    def __init__(self, nick, server, sasl_username=None, sasl_password=None, **kwargs):
        super().__init__(nick, sasl_username=sasl_username, sasl_password=sasl_password, **kwargs)
        self.server = server
    
    async def on_raw(self, message):
        # print(message._raw.split()[1])
        # print(message.params[0])
        await super().on_raw(message)
    
    async def on_nick_change(self, old, new):
        if old == self.server.nick:
            print(f'changing my nick from {old} to {new}')
            self.server.on_own_nick_change(new)
        await super().on_nick_change(old, new)
    
    async def on_join(self, channel, user):
        print(f'User {user} joined {channel}')
        if user == self.server.nick:
            self.server.on_join_channel(channel)
        await super().on_join(channel, user)


    async def on_message(self, target, source, message):
        self.server.on_rcvd_message(target, source, message)
        await super().on_message(target, source, message)
    
    async def on_ctcp_action(self, by, target, contents):
        print(f'action: by={by}, target={target}, contents={contents}')
        message = f'{by} {contents}'
        self.server.on_rcvd_message(target, '*', message)