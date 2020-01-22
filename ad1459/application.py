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

from .formatting import Parser
from .network import Network
from .widgets.window import Ad1459Window
from . import handlers

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
        self.app.parser = Parser()
        self.parser = Parser()

                # Set up CSS
        css = (
            b'.message-row {'
            b'  border-radius: 6px;'
            b'  background-color: alpha(@theme_selected_bg_color, 0.1);'
            b'}'
            b'.mine {'
            b'  background-color: alpha(@theme_selected_bg_color, 0.2);'
            b'}'
            b'.highlight {'
            b'    background-color: alpha(@success_color, 0.3);'
            b'}'
            b'.server {'
            b'    background-color: transparent;'
            b'}'
            b'.notice {'
            b'    background-color: alpha(@warning_color, 0.3);'
            b'}'
            b'.connect-entry {'
            b'    background-color: @theme_base_color;'
            b'}'
            b'.topic-expander {'
            b'    font-size: 0.75em;'
            b'}'
        )

        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

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
        window.props.application = self.app
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
        # Hook up the IRC Entry and related buttons
        window.irc_entry.connect(
            'activate', 
            handlers.on_send_button_clicked,
            window.irc_entry.get_text(),
            window.switcher.get_active_room(),
            window
        )
        window.send_button.connect(
            'clicked', 
            handlers.on_send_button_clicked,
            window.irc_entry.get_text(),
            window.switcher.get_active_room(),
            window
        )
        window.nick_button.connect(
            'clicked',
            handlers.on_nick_button_clicked,
            window
        )

        # Hook up header functions
        window.header.close_button.connect(
            'clicked',
            handlers.on_appmenu_close_clicked,
            window.switcher.get_active_room(),
            window
        )
        # window.header.keys_button.connect(
        #     'clicked',
        #     handlers.on_appmenu_keys_clicked,
        #     window
        # )
        window.header.about_button.connect(
            'clicked',
            handlers.on_appmenu_about_clicked,
            window
        )

        # ServerPopup functions
        window.header.server_popup.connect_button.connect(
            'clicked',
            handlers.on_server_popup_connect_clicked,
            window
        )

        # Channel Switcher 
        window.switcher.switcher.connect(
            'row-selected',
            handlers.on_room_selected,
            window
        )
        window.join_entry.connect(
            'activate',
            handlers.on_join_entry_activate,
            window
        )
        window.join_entry.connect(
            'icon-release',
            handlers.on_join_entry_icon_release,
            window
        )

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

    # def add_network(
    #         self,
    #         name=None,
    #         auth=None,
    #         host=None,
    #         port=None,
    #         tls=True,
    #         nick=None,
    #         user=None,
    #         real=None,
    #         pasw=None
    # ):
    #     """ Adds a network object to this application.

    #     Returns:
    #         A :obj:`Network` for the new network.
    #     """
    #     new_network = Network(self)
        
    #     if name:
    #         new_network.name = name

    #     if auth:
    #         new_network.auth = auth

    #     if host:
    #         new_network.host = host

    #     if port:
    #         new_network.port = port

    #     if not tls:
    #         new_network.tls = tls

    #     if nick:
    #         new_network.nickname = nick

    #     if user:
    #         new_network.username = user

    #     if real:
    #         new_network.realname = real

    #     if pasw:
    #         new_network.password = pasw
