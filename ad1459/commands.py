#!/usr/bin/env python3

""" AD1459, an IRC Client

  Copyright ©2019-2020 by Gaven Royer

  Permission to use, copy, modify, and/or distribute this software for any
  purpose with or without fee is hereby granted, provided that the above
  copyright notice and this permission notice appear in all copies.

  THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH REGARD
  TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
  FITNESS. IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
  CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
  ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
  SOFTWARE.

  Commands and their actions.
"""

import asyncio
import logging

class Commands:
    """ Commands for IRC.

    Each method in this class is a command to run. It should complete the 
    action required by the command.
    """
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
