#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Main Application
"""

import asyncio
import logging
import pathlib
import os
import threading

import gi
gi.require_versions(
    {
        'Gtk': '3.0',
        'Gdk': '3.0'
    }
)
from gi.repository import Gtk, Gdk, Gio

from.formatting import Parser
from .network import Network
from .widgets.window import Ad1459Window

USER_HOME_PATH = str(pathlib.Path.home())
CONFIG_DIR_PATH = os.path.join(
    USER_HOME_PATH, 
    os.path.join('.config', 'ad1459')
)
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR_PATH, 'servers.ini')

class Ad1459Application:

    def __init__(self):
        self.log = logging.getLogger('ad1459')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)
        self.log.debug('Initializing application')

        self.user_home_path = USER_HOME_PATH
        self.config_dir_path = CONFIG_DIR_PATH
        self.config_file_path = CONFIG_FILE_PATH

        self.windows = []
        self.networks = []

        self.app = Gtk.Application.new(
            'in.donotspellitgav.in', Gio.ApplicationFlags.FLAGS_NONE
        )
        self.app.connect('activate', self.init_application)
        self.parser = Parser()

    def init_application(self):
        """ Starts up all of the application loops and peices."""
        self.log.debug('Initializing IRC thread')
        self.irc = threading.Thread(target=asyncio.get_event_loop().run_forever)
        self.irc.daemon = True
        self.irc.start()

        self.log.debug('Creating initial window...')
        first_window = self.init_window()
        self.windows.append(first_window)
        first_window.show_all()

        self.log.debug('Starting up GTK main loop.')
        Gtk.main()

    def init_window(self):
        """ Create a a window for the application.
        
        Returns:
            A Gtk.Window set up for AD1459
        """
        self.log.debug('Adding window')
        window = Ad1459Window(self)
        window.set_default_size(1000, 600)
        window.connect('delete-event', self.remove_window)
        self.connect_ui(window)
        
        window.show_all()
        return window

    def connect_ui(self, window):
        """ Connects the UI in window to the correct signal handlers.

        Arguments:
            window (:obj:`Ad1459Windw`): The window object to connect.
        """

    def remove_window(self, window, data=None):
        """ Deletes a window and moves all of its stuff to another window.

        Arguments: 
            window (Gtk.Window): The window to remove.
        """
        self.log.debug('Deleting window')
        window.destroy()

        if len(self.windows) <= 1:
            self.log.debug('Last window destroyed, quitting.')
            Gtk.main_quit()
            exit(0)

    def add_network(
            self,
            name=None,
            auth=None,
            host=None,
            port=None,
            tls=True,
            nick=None,
            user=None,
            real=None,
            pasw=None
    ):
        """ Adds a network object to this application.

        Returns:
            A :obj:`Network` for the new network.
        """
        new_network = Network(self)
        
        if name:
            new_network.name = name

        if auth:
            new_network.auth = auth

        if host:
            new_network.host = host

        if port:
            new_network.port = port

        if not tls:
            new_network.tls = tls

        if nick:
            new_network.nickname = nick

        if user:
            new_network.username = user

        if real:
            new_network.realname = real

        if pasw:
            new_network.password = pasw
