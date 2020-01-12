#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Commands and their actions.
"""

import asyncio
import logging

class Commands:
    log = logging.getLogger('ad1459.commands')
    def me(self, room, client, message):
        """ /me command

        Sends a CTCP Action.

        Arguments:
            room (:obj:`Room`): The room to ACTION
            client (:obj:`Client`): The client object
            message (str): The action to send.
        """
        amessage = ' '.join(message.split()[1:])
        self.log.debug('Sending action to %s: %s', room.name, amessage)
        asyncio.run_coroutine_threadsafe(
            client.ctcp(room.name, 'ACTION', contents=amessage),
            loop=asyncio.get_event_loop()
        )
