#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the main module. When imported, it should run the application and 
  spawn the GUI.
"""

import asyncio
import logging
import pydle
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

# from .window import AdWindow
        

# app = Gtk.Application.new(
#   'in.donotspellitgav.ad1459', Gio.ApplicationFlags.FLAGS_NONE
# )

# print('Setting up logging')
# log = logging.getLogger('ad1459')
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)
# log.debug('Initializing application')

# app.nick = "ad1459"
# app.username = 'ad1459'
# app.realname = 'AD1459 User'

# app.window = AdWindow(app)
# app.window.set_default_size(1000,600)
# app.window.connect('delete-event', Gtk.main_quit)
# app.window.show_all()

# log.debug('Initializing IRC thread')
# irc = threading.Thread(target=asyncio.get_event_loop().run_forever)
# irc.daemon = True
# irc.start()

# log.debug('Starting GTK Main Loop')
# Gtk.main()

# app.run()