#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Signal handlers for UI components.
"""

import logging

from .nunetwork import Network

def on_send_button_clicked(widget, text, room, window, data=None):
    """ `clicked` signal handler for the Send button.

    Also handles the `activate` signal for the IRC Entry.
    
    Arguments:
        text (str): The text to send to IRC.
        room (:obj:`Room`): The room to send `text` to.
        window (:obj:`Ad1459Application`): The window we're in
    """
    log = logging.getLogger('ad1459.handlers.send_button_clicked')
    log.debug('!')

def on_nick_button_clicked(button, text, network, window, data=None):
    """`clicked` signal handler for the nickname button.
    
    Arguments:
        text (str): The text to set the nickname to.
        network (:obj:`Network`): The network whose nick to set.
        window (:obj:`Ad1459Application`): The window we're in
    """
    log = logging.getLogger('ad1459.handlers.nick_button_clicked')
    log.debug('!')

def on_server_popup_connect_clicked(button, window, data=None):
    """`clicked` signal handler for the Connect button in the server popup
    
    Arguments:
        window (:obj:`Ad1459Application`): The window we're in
    """
    log = logging.getLogger('ad1459.handlers.server_popup_connect_clicked')
    popup = window.header.server_popup
    app = window.app
    network_line = popup.server_line
    
    if network_line:
        pass

    else:
        network = Network(app)
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
    
    log.info('Connecting to %s:%s', network.host, network.port)
    network.connect()
    popup.layout_grid.set_sensitive(False)

def on_appmenu_close_clicked(button, room, window, data=None):
    """`clicked` signal handler for the Leave button in the appmenu.
    
    Arguments:
        room (:obj:`Room`): The Room to leave.
        window (:obj:`Ad1459Application`): The window we're in
    """
    log = logging.getLogger('ad1459.handlers.appmenu_close_clicked')
    log.debug('!')

def on_appmenu_about_clicked(button, window, data=None):
    """`clicked` signal handler for the About button.
    
    Arguments:
        window (:obj:`Ad1459Application`): The window we're in
    """
    log = logging.getLogger('ad1459.handlers.appmenu_about_clicked')
    log.debug('!')