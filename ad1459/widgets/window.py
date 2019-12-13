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

from .headerbar import Headerbar
from .message_row import MessageRow
from .room_row import RoomRow

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
        servers_window.add(self.servers_listbox)
        
        message_grid = Gtk.Grid()
        content.add2(message_grid)
        message_window = Gtk.ScrolledWindow()
        message_window.set_hexpand(True)
        message_window.set_vexpand(True)
        message_grid.attach(message_window, 0, 0, 1, 1)

        entry_box = Gtk.Box()
        entry_box.props.margin = 2
        message_grid.attach(entry_box, 0, 1, 1, 1)

        message_entry = Gtk.Entry()
        message_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY,
            'mail-send-symbolic'
        )
        message_entry.set_hexpand(True)
        # message_entry.props.show_emoji_icon = True
        message_grid.props.margin = 2
        entry_box.add(message_entry)

        self.messages = Gtk.ListBox()
        message_window.add(self.messages)

        self.populate_test_data()
        
    def populate_test_data(self):
        test_server1 = RoomRow('server')
        test_server1.room_name = 'Esper'
        self.servers_listbox.add(test_server1)
        
        test_server2 = RoomRow('room')
        test_server2.room_name = '#lobby'
        self.servers_listbox.add(test_server2)
        
        test_server6 = RoomRow('user')
        test_server6.room_name = 'LordRyan'
        self.servers_listbox.add(test_server6)
        
        test_server3 = RoomRow('server')
        test_server3.room_name = 'freenode'
        self.servers_listbox.add(test_server3)
        
        test_server4 = RoomRow('room')
        test_server4.room_name = '##fosters'
        self.servers_listbox.add(test_server4)
        
        test_server5 = RoomRow('room')
        test_server5.room_name = '##iciloo'
        self.servers_listbox.add(test_server5)
        
        test_server6 = RoomRow('room')
        test_server6.room_name = '##werewolf'
        self.servers_listbox.add(test_server6)

        test_message = MessageRow()
        test_message.time = '25:67'
        test_message.sender = 'jeans'
        test_message.text = ('Hi')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:67'
        test_message.sender = 'gav'
        test_message.text = ('hoi')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:68'
        test_message.sender = 'jeans'
        test_message.text = ('How are things')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:69'
        test_message.sender = 'gav'
        test_message.text = ('Okay')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:70'
        test_message.sender = 'jeans'
        test_message.text = (
            'This is a really long message that I want to send because I want '
            'to see what it looks like in-context. Now it\'s going to be really '
            'long, yay!'
        )
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:70'
        test_message.sender = 'gav'
        test_message.text = ('wow spam')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:71'
        test_message.sender = 'notgav'
        test_message.text = ('rood')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:72'
        test_message.sender = 'jeans'
        test_message.text = ('sorry')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:67'
        test_message.sender = 'jeans'
        test_message.text = (
            'Now it\'s even longer and it will run off the edge of the boundary '
            'so that I can see what it will look like really long. '
            'This is a really long message that I want to send because I want '
            'to see what it looks like in-context. Now it\'s going to be really '
            'long, yay!'
        )
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:67'
        test_message.sender = 'gav'
        test_message.text = ('hoi')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:68'
        test_message.sender = 'jeans'
        test_message.text = ('How are things')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:69'
        test_message.sender = 'gav'
        test_message.text = ('Okay')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:70'
        test_message.sender = 'jeans'
        test_message.text = (
            'This is a really long message that I want to send because I want '
            'to see what it looks like in-context. Now it\'s going to be really '
            'long, yay!'
        )
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:70'
        test_message.sender = 'gav'
        test_message.text = ('wow spam')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:71'
        test_message.sender = 'notgav'
        test_message.text = ('rood')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:72'
        test_message.sender = 'jeans'
        test_message.text = ('sorry')
        self.messages.add(test_message)
        