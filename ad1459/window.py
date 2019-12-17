#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This file is the application window.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .widgets.headerbar import Headerbar
from .room import Room

class AdWindow(Gtk.Window):
    """ The main application window."""

    def __init__(self):
        Gtk.Window.__init__(self)
        header = Headerbar()
        self.set_titlebar(header)

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

        message_entry = Gtk.Entry()
        message_entry.set_hexpand(True)
        message_entry.set_placeholder_text('Enter a message')
        message_entry.connect('activate', self.on_send_button_clicked, message_entry)
        message_entry.props.show_emoji_icon = True
        message_entry.props.max_width_chars = 5000

        self.nick_button = Gtk.Button.new_with_label('jeans')
        self.nick = 'user'
        self.nick_button.set_halign(Gtk.Align.START)
        self.nick_button.connect('clicked', self.on_nick_button_clicked, message_entry)
        Gtk.StyleContext.add_class(self.nick_button.get_style_context(), 'flat')

        entry_box.add(self.nick_button)
        entry_box.add(message_entry)

        send_button = Gtk.Button.new_from_icon_name(
            'mail-send-symbolic',
            Gtk.IconSize.BUTTON
        )
        send_button.set_hexpand(False)
        send_button.set_halign(Gtk.Align.END)
        send_button.connect('clicked', self.on_send_button_clicked, message_entry)
        Gtk.StyleContext.add_class(
            send_button.get_style_context(), 
            'suggested-action'
        )
        entry_box.add(send_button)

        self.populate_test_data()
    
    @property
    def nick(self):
        """str: The current user's nickname."""
        return self.nick_button.get_label()
    
    @nick.setter
    def nick(self, nick):
        """ We just store this on the nickname button for convenience."""
        self.nick_button.set_label(nick)
    
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
        room = self.get_active_room()
        room.add_message(message_text, sender=self.nick, css='mine')
        self.show_all()
        entry.set_text('')

    def get_active_room(self):
        """ Gets the name of the currently active room. """
        current_row = self.servers_listbox.get_selected_row()
        return current_row.room
    
    def on_server_selected(self, listbox, row):
        """ row-selected signal handler for server_listbox.

        Arguments:
            listbox (:obj:`Gtk.ListBox`): The server_listbox
            row (:obj:`Gtk.ListBoxRow`): The row the user clicked on.
        """
        new_room = row.room_name
        self.message_stack.set_visible_child_name(new_room)
    
    def on_new_message_scroll(self, widget, data=None):
        """ Handler to keep the window scrolled to the bottom of the buffer."""
        adj = self.message_window.get_vadjustment()
        adj.set_value(adj.props.upper - adj.props.page_size)
        
    def populate_test_data(self):
        test_room1 = Room()
        test_room1.name = 'Esper'
        test_room1.row.kind = 'server'
        self.servers_listbox.add(test_room1.row)
        self.message_stack.add_named(test_room1.window, test_room1.name)

        test_room2 = Room()
        test_room2.name = '#lobby'
        self.servers_listbox.add(test_room2.row)
        self.message_stack.add_named(test_room2.window, test_room2.name)

        test_room3 = Room()
        test_room3.name = 'freenode'
        test_room3.row.kind = 'server'
        self.servers_listbox.add(test_room3.row)
        self.message_stack.add_named(test_room3.window, test_room3.name)

        test_room4 = Room()
        test_room4.name = '##club_nomicon'
        self.servers_listbox.add(test_room4.row)
        self.message_stack.add_named(test_room4.window, test_room4.name)

        test_room5 = Room()
        test_room5.name = '##fosters'
        self.servers_listbox.add(test_room5.row)
        self.message_stack.add_named(test_room5.window, test_room5.name)
        