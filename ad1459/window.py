#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This file is the application window.
"""

import asyncio

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .widgets.headerbar import Headerbar
from .room import Room
from .server import Server

class AdWindow(Gtk.Window):
    """ The main application window."""

    def __init__(self, app):
        super().__init__()
        self.servers = []
        self.app = app
        header = Headerbar()
        self.set_titlebar(header)

        server_button = Gtk.Button.new_from_icon_name(
            'network-server-symbolic',
            Gtk.IconSize.BUTTON
        )
        server_button.connect('clicked', self.on_server_button_clicked)
        header.pack_start(server_button)

        channel_button = Gtk.Button.new_from_icon_name(
            'list-add-symbolic',
            Gtk.IconSize.BUTTON
        )
        channel_button.connect('clicked', self.on_channel_button_clicked)
        header.pack_start(channel_button)

        # Set up CSS
        css = (
            b'.message-row {'
            b'  margin: 3px;'
            b'  border-radius: 6px;'
            b'  background-color: alpha(@theme_selected_bg_color, 0.1);'
            b'}'
            b'.mine {'
            b'  background-color: alpha(@theme_selected_bg_color, 0.2);'
            b'}'
        )

        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        maingrid = Gtk.Grid()
        self.add(maingrid)

        content = Gtk.HPaned()
        content.set_position(200)
        content.set_hexpand(True)
        content.set_vexpand(True)
        maingrid.attach(content, 0, 0, 1, 1)

        servers_grid = Gtk.Grid()
        content.add1(servers_grid)
        servers_window = Gtk.ScrolledWindow()
        servers_window.set_hexpand(True)        
        servers_window.set_vexpand(True)
        servers_grid.attach(servers_window, 0, 0, 1, 1)

        self.servers_listbox = Gtk.ListBox()
        self.servers_listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)
        self.servers_listbox.connect('row-selected', self.on_server_selected)
        servers_window.add(self.servers_listbox)
        
        message_grid = Gtk.Grid()
        content.add2(message_grid)

        self.message_stack = Gtk.Stack()
        self.message_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.message_stack.set_transition_duration(100)
        message_grid.attach(self.message_stack, 0, 0, 1, 1)

        entry_box = Gtk.HBox()
        entry_box.props.margin = 6
        entry_box.props.spacing = 6
        message_grid.attach(entry_box, 0, 1, 1, 1)

        self.message_entry = Gtk.Entry()
        self.message_entry.set_hexpand(True)
        self.message_entry.set_placeholder_text('Enter a message')
        self.message_entry.connect('activate', self.on_send_button_clicked, self.message_entry)
        self.message_entry.props.show_emoji_icon = True
        self.message_entry.props.max_width_chars = 5000

        self.nick_button = Gtk.Button.new_with_label('jeans')
        self.nick = 'user'
        self.nick_button.set_halign(Gtk.Align.START)
        self.nick_button.connect('clicked', self.on_nick_button_clicked, self.message_entry)
        Gtk.StyleContext.add_class(self.nick_button.get_style_context(), 'flat')

        entry_box.add(self.nick_button)
        entry_box.add(self.message_entry)

        send_button = Gtk.Button.new_from_icon_name(
            'mail-send-symbolic',
            Gtk.IconSize.BUTTON
        )
        send_button.set_hexpand(False)
        send_button.set_halign(Gtk.Align.END)
        send_button.connect('clicked', self.on_send_button_clicked, self.message_entry)
        Gtk.StyleContext.add_class(
            send_button.get_style_context(), 
            'suggested-action'
        )
        entry_box.add(send_button)

        # self.populate_test_data()
    
    def on_channel_button_clicked(self, button, data=None):
        """ clicked signal handler for channel button."""
        self.join_channel(self.message_entry.get_text())
        self.message_entry.set_text('')
    
    def on_server_button_clicked(self, button, data=None):
        """ clicked signal handler for the server button."""
        self.add_server(self.message_entry.get_text())
        self.message_entry.set_text('')
    
    def on_nick_button_clicked(self, button, entry):
        """ clicked signal handler for nickname button.

        Arguments:
            button (:obj:`Gtk.Button`): The button the user clicked.
            entry (:obj:`Gtk.Entry`): The chat entry with the new nickname.
        """
        new_nick = entry.get_text()
        self.nick = new_nick
        entry.set_text('')
    
    def on_send_button_clicked(self, button, entry):
        """ clicked signal handler for send button.

        Arguments:
            button (:obj:`Gtk.Button`): The send button the user clicked.
            entry (:obj:`Gtk.Entry`): The chat entry with the message.
        """
        message_text = entry.get_text()
        room = self.get_active_room(room='current')
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(
            room.server.client.message(room.name, message_text),
            loop=loop
        )
        # room.add_message(message_text, sender=self.nick, css='mine')
        # self.show_all()
        entry.set_text('')
    
    def join_channel(self, channel_name, server='current'):
        """ Joins a channel on the current server.
        
        Arguments:
            channel_name (str): The name of the channel to join.
        """
        print(f'Joining {channel_name}...')
        current_server = self.get_active_server(server)
        current_server.join_room(channel_name)
        self.servers_listbox.add(current_server.rooms[-1].row)
        self.message_stack.add_named(
            current_server.rooms[-1].window, current_server.rooms[-1].name
        )
        self.show_all()
    
    def add_server(self, server_line):
        """ Adds a new server to the list.
        
        Arguments:
            server_name (str): The name for this server
            host (str): The hostname of this server, or 'test'
        """
        # Format is servername host port nick (tls) (password=(password))
        server_list = server_line.split()
        new_server = Server(self.app, server_list[3])
        new_server.name = server_list[0]
        new_server.host = server_list[1]
        new_server.port = int(server_list[2])
        if server_list[4] == 'tls':
            new_server.tls = True
        if 'password=' in server_list[-1]:
            new_server.password = server_list[-1].split('=')[1]
        
        self.servers.append(new_server)
        new_server.connect()
        self.servers_listbox.add(new_server.room.row)
        self.message_stack.add_named(new_server.room.window, new_server.name)
        self.show_all()

    def get_active_room(self, room='current'):
        """ Gets the currently active room object. """
        print(f'Getting room for {room}')
        if room == 'current':
            return self.message_stack.get_visible_child().room
        else:
            return self.message_stack.get_child_by_name(room).room
    
    def get_active_server(self, server='current'):
        """ Gets the server object for the currently active room."""
        if server == 'current':
            return self.message_stack.get_visible_child().server
        else:
            return self.message_stack.get_child_by_name(server).server
    
    def on_server_selected(self, listbox, row):
        """ row-selected signal handler for server_listbox.

        Arguments:
            listbox (:obj:`Gtk.ListBox`): The server_listbox
            row (:obj:`Gtk.ListBoxRow`): The row the user clicked on.
        """
        new_room = row.room_name
        row.unread_indicator.set_visible(False)
        self.message_stack.set_visible_child_name(new_room)
        
    def populate_test_data(self):
        """ Currently empty, but allows quick population of data for 
        screenshots and similar.
        """
        