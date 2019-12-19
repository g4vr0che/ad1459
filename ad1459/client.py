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

    def __init__(self, nick, server):
        super().__init__(nick)
        self.server = server
    
    async def on_connect(self):
        await asyncio.sleep(2)
        for channel in self.channels:
            print(f'joining {channel}')
            self.server.on_join_channel(channel)
        await asyncio.sleep(2)
        

        await super().on_connect()

    async def on_message(self, target, source, message):
        self.server.on_rcvd_message(target, source, message)
        await super().on_message(target, source, message)
        