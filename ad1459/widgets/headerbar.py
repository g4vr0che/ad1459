#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the headerbar.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .server_popup import ServerPopover

class Headerbar(Gtk.HeaderBar):
    """ The headerbar we use."""

    def __init__(self, app):
        super().__init__()

        self.set_show_close_button(True)
        self.set_title('AD1459')
        self.set_has_subtitle(False)

        self.network_button = Gtk.MenuButton()
        network_image = Gtk.Image.new_from_icon_name(
            'network-server-symbolic',
            Gtk.IconSize.BUTTON
        )
        self.network_button.set_image(network_image)
        self.pack_start(self.network_button)

        self.server_popup = ServerPopover(app.config_file_path)
        self.server_popup.show_all()
        self.server_popup.popdown()
        self.network_button.set_popover(self.server_popup)

        self.spinner = Gtk.Spinner()
        self.pack_start(self.spinner)

        self.appmenu = Gtk.Popover()
        appmenu_grid = Gtk.Grid()
        appmenu_grid.set_margin_start(6)
        appmenu_grid.set_margin_end(6)
        appmenu_grid.set_margin_top(6)
        appmenu_grid.set_margin_bottom(6)
        self.appmenu.add(appmenu_grid)

        self.close_button = Gtk.ModelButton()
        self.close_button.set_label('Close conversation')
        appmenu_grid.attach(self.close_button, 0, 0, 1, 1)

        self.about_button = Gtk.ModelButton()
        self.about_button.set_label('About AD1459')
        appmenu_grid.attach(self.about_button, 0, 1, 1, 1)

        self.appmenu.show_all()
        self.appmenu.popdown()

        appmenu_button = Gtk.MenuButton()
        appmenu_image = Gtk.Image.new_from_icon_name(
          'view-more-symbolic',
          Gtk.IconSize.BUTTON
        )
        appmenu_button.set_image(appmenu_image)
        appmenu_button.set_popover(self.appmenu)
        self.pack_end(appmenu_button)
