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
        content.set_position(300)
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

        self.messages = Gtk.ListBox()
        servers_window.add(self.messages)
        
    def populate_test_data(self):
        test_server1 = RoomRow()
        test_server1.name = 'Esper'
        self.servers_listbox.add(test_server1)
        
        test_server2 = RoomRow()
        test_server2.name = '#lobby'
        test_server2.props.margin_bottom = 24
        self.servers_listbox.add(test_server2)
        
        test_server3 = RoomRow()
        test_server3.name = 'freenode'
        self.servers_listbox.add(test_server3)
        
        test_server4 = RoomRow()
        test_server4.name = '##fosters'
        self.servers_listbox.add(test_server4)
        
        test_server5 = RoomRow()
        test_server5.name = '##iciloo'
        self.servers_listbox.add(test_server5)
        
        test_server6 = RoomRow()
        test_server6.name = '##werewolf'
        self.servers_listbox.add(test_server6)

        test_message = MessageRow()
        test_message.time = '25:67'
        test_message.sender = 'jeans'
        test_message.message = ('Hi')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:67'
        test_message.sender = 'gav'
        test_message.message = ('hoi')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:68'
        test_message.sender = 'jeans'
        test_message.message = ('How are things')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:69'
        test_message.sender = 'gav'
        test_message.message = ('Okay')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:70'
        test_message.sender = 'jeans'
        test_message.message = (
            'This is a really long message that I want to send because I want '
            'to see what it looks like in-context. Now it\'s going to be really '
            'long, yay!'
        )
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:70'
        test_message.sender = 'gav'
        test_message.message = ('wow spam')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:71'
        test_message.sender = 'notgav'
        test_message.message = ('rood')
        self.messages.add(test_message)

        test_message = MessageRow()
        test_message.time = '25:72'
        test_message.sender = 'jeans'
        test_message.message = ('sorry')
        self.messages.add(test_message)
        