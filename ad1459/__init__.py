#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  This is the main module.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .window import AdWindow

class AdApplication(Gtk.Application):

    def do_activate(self):
         self.window = AdWindow()
         self.window.set_default_size(1000,600)
         self.window.connect('delete-event', Gtk.main_quit)
         self.window.show_all()

         Gtk.main()

app = AdApplication()
app.run()