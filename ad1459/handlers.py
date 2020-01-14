#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Signal handlers for UI components.
"""

import logging

from .network import Network
from .widgets.room_row import RoomKind
from .widgets.about import AboutDialog

def on_send_button_clicked(widget, text, room, window, data=None):
    """ `clicked` signal handler for the Send button.

    Also handles the `activate` signal for the IRC Entry.
    
    Arguments:
        text (str): The text to send to IRC.
        room (:obj:`Room`): The room to send `text` to.
        window (:obj:`Ad1459Application`): The window we're in
    """
    room = window.message_stack.get_visible_child().room
    network = room.network
    message = window.irc_entry.get_text()
    if message:
        network.send_message(room, message)
    window.irc_entry.set_text('')

def on_nick_button_clicked(button, window, data=None):
    """`clicked` signal handler for the nickname button.
    
    Arguments:
        text (str): The text to set the nickname to.
        network (:obj:`Network`): The network whose nick to set.
        window (:obj:`Ad1459Application`): The window we're in
    """
    network = window.active_room.network
    new_nick = window.irc_entry.get_text()
    network.change_nick(new_nick)
    window.irc_entry.set_text('')

def on_server_popup_connect_clicked(button, window, data=None):
    """`clicked` signal handler for the Connect button in the server popup
    
    Arguments:
        window (:obj:`Ad1459Application`): The window we're in
    """
    popup = window.header.server_popup
    app = window.app
    network_line = popup.server_line
    window.header.spinner.start()
    
    if network_line:
        pass

    else:
        network = Network(app, window)
        network.name = popup.name
        network.auth = popup.auth
        network.host = popup.server
        network.port = popup.port
        network.tls = popup.tls
        network.nickname = popup.nick
        network.username = popup.username
        network.realname = popup.realname
        network.password = popup.password
    
    app.networks.append(network)
    
    if popup.save:
        popup.save_details()

    network.connect()
    popup.popdown()
    popup.layout_grid.set_sensitive(False)

def on_appmenu_close_clicked(button, room, window, data=None):
    """`clicked` signal handler for the Leave button in the appmenu.
    
    Arguments:
        room (:obj:`Room`): The Room to leave.
        window (:obj:`Ad1459Application`): The window we're in
    """
    room = window.message_stack.get_visible_child().room
    network = room.network
    if room.kind == RoomKind.CHANNEL:
        room.part()
    elif room.kind == RoomKind.SERVER:
        for room in network.rooms:
            room.leave()
        room.network.disconnect()
        window.app.networks.remove(network)
        window.switcher.invalidate_sort()
    else:
        room.network.rooms.remove(room)
        room.leave()
        window.switcher.invalidate_sort()


def on_appmenu_about_clicked(button, window, data=None):
    """`clicked` signal handler for the About button.
    
    Arguments:
        window (:obj:`Ad1459Application`): The window we're in
    """
    about_dialog = AboutDialog()
    about_dialog.run()
    about_dialog.destroy()

def on_room_selected(listbox, row, window, data=None):
    """`row-selected` signal handler for room switcher.

    Arguments:
        window (:obj:`Gtk.Window`): The window we're part of.
    """
    try:
        row.room.update_users()
        row.room.topic_pane.update_topic()
        row.room.notification.close()
        window.show_all()
        row.set_icon('radio-symbolic')
        window.message_stack.set_visible_child_name(row.room.id)
        window.topic_stack.set_visible_child_name(row.room.id)
        window.irc_entry.grab_focus_without_selecting()
        window.nick_button.set_label(row.room.network.nickname)
        
        if row.room.kind == RoomKind.DIALOG:
            window.header.close_button.set_label('Close conversation')
        
        elif row.room.kind == RoomKind.SERVER:
            window.header.close_button.set_label('Disconnect from server')
        
        elif row.room.kind == RoomKind.CHANNEL:
            window.header.close_button.set_label('Leave channel')
    
    except AttributeError:
        return
    
    window.switcher.invalidate_sort()

def on_join_entry_activate(entry, window, data=None):
    """`activate` signal handler for join entry.

    also handles the `icon-release` signal.
    """
    room_name = entry.get_text()
    network = window.message_stack.get_visible_child().room.network
    
    if room_name.startswith('#'):
        network.join_channel(room_name)
    
    else:
        room = network.get_room_for_name(room_name)

    
    entry.set_text('')
    

