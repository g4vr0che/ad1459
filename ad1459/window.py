#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This file is the application window.
"""

import asyncio
import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .widgets.headerbar import Headerbar
from .widgets.room_row import RoomKind, room_row_sort
from .widgets.irc_entry import IrcEntry
from .widgets.about import AboutDialog
from .formatting import Parser
from .room import Room
from .network import Network

class AdWindow(Gtk.Window):
    """ The main application window."""

    def __init__(self, app):
        self.log = logging.getLogger('ad1459.window')
        self.commands = {
            '/me': self.send_action
        }

        self.log.debug('Creating window')
        super().__init__()
        self.networks = []
        self.app = app
        header = Headerbar()
        self.set_titlebar(header)

        network_button = Gtk.Button.new_from_icon_name(
            'network-server-symbolic',
            Gtk.IconSize.BUTTON
        )
        network_button.connect('clicked', self.on_network_button_clicked)
        header.pack_start(network_button)

        btn_appmenu = Gtk.MenuButton()
        header.pack_end(btn_appmenu)

        self.appmenu = Gtk.Popover()
        btn_appmenu.set_popover(self.appmenu)
        am_grid = Gtk.Grid()
        am_grid.props.margin = 6
        self.appmenu.add(am_grid)

        part_button = Gtk.ModelButton()
        part_button.set_label('Leave Conversation')
        part_button.connect('clicked', self.on_part_button_clicked)
        am_grid.attach(part_button, 0, 0, 1, 1)

        about_button = Gtk.ModelButton()
        about_button.set_label('About AD1459')
        about_button.connect('clicked', self.on_about_button_clicked)
        am_grid.attach(about_button, 0, 1, 1, 1)

        self.appmenu.show_all()

        self.network_popup = Gtk.Popover()
        network_popup_grid = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        Gtk.StyleContext.add_class(network_popup_grid.get_style_context(), 'linked')
        network_popup_grid.props.margin = 6
        self.network_popup.add(network_popup_grid)

        network_entry = Gtk.Entry()
        network_entry.set_placeholder_text('Enter a network to connect to')
        network_entry.set_width_chars(80)
        network_popup_grid.pack_start(network_entry, False, True, 0)
        network_entry.connect('activate', self.on_network_connect_clicked, network_entry)

        network_connect = Gtk.Button()
        network_connect.set_label('Connect')
        Gtk.StyleContext.add_class(network_connect.get_style_context(), 'suggested-action')
        network_connect.connect('clicked', self.on_network_connect_clicked, network_entry)
        network_popup_grid.pack_end(network_connect, False, True, 0)

        channel_button = Gtk.Button.new_from_icon_name(
            'list-add-symbolic',
            Gtk.IconSize.BUTTON
        )
        channel_button.connect('clicked', self.on_channel_button_clicked)
        header.pack_start(channel_button)

        self.chan_popup = Gtk.Popover()
        chan_popup_grid = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        Gtk.StyleContext.add_class(chan_popup_grid.get_style_context(), 'linked')
        chan_popup_grid.props.margin = 6
        self.chan_popup.add(chan_popup_grid)

        channel_entry = Gtk.Entry()
        channel_entry.set_placeholder_text('Enter a channel to join')
        channel_entry.set_width_chars(40)
        chan_popup_grid.add(channel_entry)
        channel_entry.connect('activate', self.on_channel_join_clicked, channel_entry)

        channel_join = Gtk.Button()
        channel_join.set_label('Join')
        Gtk.StyleContext.add_class(channel_join.get_style_context(), 'suggested-action')
        channel_join.connect('clicked', self.on_channel_join_clicked, channel_entry)
        chan_popup_grid.add(channel_join)

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

        networks_grid = Gtk.Grid()
        content.add1(networks_grid)
        networks_window = Gtk.ScrolledWindow()
        networks_window.set_hexpand(True)        
        networks_window.set_vexpand(True)
        networks_grid.attach(networks_window, 0, 0, 1, 1)

        self.networks_listbox = Gtk.ListBox()
        self.networks_listbox.set_sort_func(room_row_sort)
        self.networks_listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)
        self.networks_listbox.connect('row-selected', self.on_network_selected)
        networks_window.add(self.networks_listbox)
        
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

        self.message_entry = IrcEntry(self)
        self.message_entry.connect('activate', self.on_send_button_clicked, self.message_entry)

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

        self.log.debug('Window created')

        # self.populate_test_data()
    
    def on_about_button_clicked(self, button, data=None):
        """ clicked signal handler for the about button."""
        about_dialog = AboutDialog()
        about_dialog.run()
        about_dialog.destroy()

    def on_part_button_clicked(self, button, data=None):
        """ clicked signal handler for the part button."""
        self.log.debug('Part_button clicked')
        channel = self.get_active_room()
        self.appmenu.popdown()
        self.leave_room(channel)
    
    def on_channel_button_clicked(self, button, data=None):
        """ clicked signal handler for channel button."""        
        self.chan_popup.set_relative_to(button)
        self.chan_popup.show_all()
        self.chan_popup.popup()
    
    def on_channel_join_clicked(self, button, entry, data=None):
        self.log.info('Joining channel')
        new_channel = entry.get_text()
        network = self.get_active_network()
        if new_channel.startswith('#'):
            loop = asyncio.get_event_loop()
            asyncio.run_coroutine_threadsafe(
                network.client.join(new_channel),
                loop=loop
            )
        else:
            self.log.debug('Opening new private message with %s', new_channel)
            self.join_channel(new_channel, network=network.name, kind='privmsg')
        self.message_entry.set_text('')
        self.chan_popup.popdown()

    def on_network_button_clicked(self, button, data=None):
        """ clicked signal handler for network button."""
        self.network_popup.set_relative_to(button)
        self.network_popup.show_all()
        self.network_popup.popup()
    
    def on_network_connect_clicked(self, button, entry, data=None):
        """ clicked signal handler for the network button."""
        self.log.info('Connecting to new network')
        self.add_network(entry.get_text())
        entry.set_text('')
        self.network_popup.popdown()
    
    def on_nick_button_clicked(self, button, entry):
        """ clicked signal handler for nickname button.

        Arguments:
            button (:obj:`Gtk.Button`): The button the user clicked.
            entry (:obj:`Gtk.Entry`): The chat entry with the new nickname.
        """
        new_nick = entry.get_text()
        self.log.info('New nick: %s', new_nick)
        self.change_nick(new_nick)
        entry.set_text('')
    
    def on_send_button_clicked(self, button, entry):
        """ clicked signal handler for send button.

        Arguments:
            button (:obj:`Gtk.Button`): The send button the user clicked.
            entry (:obj:`Gtk.Entry`): The chat entry with the message.
        """
        parser = Parser()
        message_text = parser.format_text(entry.get_text())
        room = self.get_active_room(room='current')
        network = room.network
        loop = asyncio.get_event_loop()
        for command in self.commands:
            if command in message_text:
                self.commands[command](message_text, room)
                pass
            elif message_text:
                asyncio.run_coroutine_threadsafe(
                    network.client.message(room.name, message_text),
                    loop=loop
                )
        self.show_all()
        entry.set_text('')
    
    def change_nick(self, new_nick):
        network = self.get_active_network()
        network.nick = new_nick
        self.log.info('Set new nick %s on network %s', new_nick, network.nick)
        loop = asyncio.get_event_loop()
        network = self.get_active_network()
        asyncio.run_coroutine_threadsafe(
            network.client.set_nickname(new_nick),
            loop=loop
        )
        self.set_nick(new_nick)
    
    def set_nick(self, new_nick):
        self.log.debug('Setting nick button label')
        self.nick_button.set_label(new_nick)
    
    def join_channel(self, channel_name, network='current', kind='channel'):
        """ Joins a channel on the current network.
        
        Arguments:
            channel_name (str): The name of the channel to join.
        """
        self.log.info(f'Joining {channel_name} on {network}')
        current_network = self.get_active_network(network=network)
        channel_type = 'privmsg'
        if channel_name.startswith('#'):
            channel_type = 'channel'
        current_network.join_room(channel_name, kind=channel_type)
        self.networks_listbox.prepend(current_network.rooms[-1].row)
        self.message_stack.add_named(
            current_network.rooms[-1].window, current_network.rooms[-1].name
        )
        self.networks_listbox.invalidate_sort()
        self.show_all()
    
    def leave_room(self, channel):
        """ leaves a room. 

        Arguments:
            channel (:obj:`Room`): The room object to leave.
        """
        self.log.debug('Leaving room %s', channel.name)
        if channel.row.kind == RoomKind.SERVER:
            # This appears to be a server room; we can't part those.
            self.log.debug('Can\'t leave server rooms')
            return False
        elif channel.row.kind == RoomKind.CHANNEL:
            channel.part_channel()
        elif channel.row.kind == RoomKind.DIALOG:
            network = self.get_active_network()
            network.remove_room_from_list(channel.name)
        self.networks_listbox.invalidate_sort()
    
    def add_network(self, network_line):
        """ Adds a new network to the list.
        
        Arguments:
            network_name (str): The name for this network
            host (str): The hostname of this network, or 'test'
        """
        # new: none|pass|sasl networkname host port username (tls) (password)
        network_list = network_line.split()
        if network_list[0] == 'sasl':
            new_network = Network(
                self.app, 
                network_list[1],
                network_list[4],
                sasl_u=network_list[4],
                sasl_p=network_list[-1]
            )
        else:
            new_network = Network(self.app, network_list[1], network_list[4])

        new_network.auth = network_list[0]
        new_network.name = network_list[1]
        new_network.host = network_list[2]
        new_network.port = int(network_list[3])
        new_network.nick = network_list[4]
        if new_network.auth == ('pass' or 'sasl'):
            new_network.password = network_list[-1]
        try:
            if network_list[5] == 'tls':
                new_network.tls = True
        except AttributeError:
            new_network.tls = False
        
        self.networks.append(new_network)
        new_network.connect()
        self.networks_listbox.add(new_network.room.row)
        self.message_stack.add_named(new_network.room.window, new_network.name)
        self.networks_listbox.invalidate_sort()
        self.show_all()
        self.set_nick(new_network.nick)

    def get_active_room(self, room='current'):
        """ Gets the currently active room object. """
        # self.log.debug('Getting room for %s', room)
        if room == 'current':
            return self.message_stack.get_visible_child().room
        else:
            return self.message_stack.get_child_by_name(room).room
    
    def get_active_network(self, network='current'):
        """ Gets the network object for the currently active room."""
        # self.log.debug('Getting network for %s', network)
        if network == 'current':
            return self.get_active_room().network
        else:
            return self.message_stack.get_child_by_name(network).room.network
    
    def on_network_selected(self, listbox, row):
        """ row-selected signal handler for network_listbox.

        Arguments:
            listbox (:obj:`Gtk.ListBox`): The network_listbox
            row (:obj:`Gtk.ListBoxRow`): The row the user clicked on.
        """
        new_room = row.room
        row.unread_indicator.set_from_icon_name(
            'mail-read-symbolic',
            Gtk.IconSize.SMALL_TOOLBAR
        )
        self.message_entry.grab_focus()
        self.log.debug(f'New room: {row.room.name} on network {row.room.network.name}')
        self.message_stack.set_visible_child_name(new_room.name)
    
    """ Commands parsed by the client."""

    def send_action(self, message, target):
        """ the IRC /me command; CTCP ACTION
        
        Arguments:
            message (str): The action to do.
            target (str): Where to send the action.
        """
        message = message.replace('/me', '', 1).strip()
        network = self.get_active_network()
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(
            network.client.ctcp(target.name, 'ACTION', message),
            loop=loop
        )

        
    def populate_test_data(self):
        """ Currently empty, but allows quick population of data for 
        screenshots and similar.
        """
        