#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This file is the application window.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .widgets.headerbar import Headerbar
from .room import Room

class AdWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        header = Headerbar()
        self.set_titlebar(header)

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
        self.servers_listbox.connect('row-selected', self.on_server_selected)
        servers_window.add(self.servers_listbox)
        
        message_grid = Gtk.Grid()
        content.add2(message_grid)
        message_window = Gtk.ScrolledWindow()
        message_window.set_hexpand(True)
        message_window.set_vexpand(True)
        message_grid.attach(message_window, 0, 0, 1, 1)

        self.message_stack = Gtk.Stack()
        self.message_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.message_stack.set_transition_duration(100)
        message_window.add(self.message_stack)

        entry_box = Gtk.HBox()
        entry_box.props.margin = 6
        entry_box.props.spacing = 6
        message_grid.attach(entry_box, 0, 1, 1, 1)

        nick_button = Gtk.Button.new_with_label('jeans')
        nick_button.set_halign(Gtk.Align.START)
        Gtk.StyleContext.add_class(nick_button.get_style_context(), 'flat')
        entry_box.add(nick_button)

        message_entry = Gtk.Entry()
        message_entry.set_hexpand(True)
        message_entry.set_placeholder_text('Enter a message')
        message_entry.connect('activate', self.on_send_button_clicked, message_entry)
        message_entry.props.show_emoji_icon = True
        message_entry.props.max_width_chars = 5000
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
    
    def on_send_button_clicked(self, button, entry):
        message_text = entry.get_text()
        room = self.get_active_room()
        room.add_message(message_text, sender='jeans')
        self.show_all()
        entry.set_text('')

    def get_active_room(self):
        current_row = self.servers_listbox.get_selected_row()
        return current_row.room
    
    def on_server_selected(self, listbox, row):
        new_room = row.room_name
        self.message_stack.set_visible_child_name(new_room)
        
    def populate_test_data(self):
        test_room1 = Room()
        test_room1.name = 'Esper'
        test_room1.row.kind = 'server'
        self.servers_listbox.add(test_room1.row)
        self.message_stack.add_named(test_room1.messages, test_room1.name)

        test_room2 = Room()
        test_room2.name = '#lobby'
        self.servers_listbox.add(test_room2.row)
        self.message_stack.add_named(test_room2.messages, test_room2.name)
        