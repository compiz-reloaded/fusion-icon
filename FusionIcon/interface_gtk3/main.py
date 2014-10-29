#!/usr/bin/env python
# This file is part of Fusion-icon.

# Fusion-icon is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Fusion-icon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Based on compiz-icon, Copyright 2007 Felix Bellanger <keeguon@gmail.com>
#
# Original author: crdlb
# GTK3 port: kozec

import os, time
from gi.repository import Gtk
from FusionIcon.start import wms, apps, options, decorators, init

class TrayMenu(Gtk.Menu):
	
	def __init__(self):
		Gtk.Menu.__init__(self)

		#CCSM
		if 'ccsm' in apps:
			item = ApplicationItem('ccsm')
			item.set_image(Gtk.Image.new_from_stock('gtk-preferences', Gtk.IconSize.MENU))
			self.append(item)

		#Emerald Theme Manager
		if 'emerald theme manager' in apps:
			item = ApplicationItem('emerald theme manager')
			item.set_image(Gtk.Image.new_from_icon_name('emerald-theme-manager-icon', Gtk.IconSize.MENU))
			self.append(item)

		if 'ccsm' in apps or 'emerald theme manager' in apps:
			item = Gtk.SeparatorMenuItem()
			self.append(item)

		#Reload
		item = Gtk.ImageMenuItem('Reload Window Manager')
		item.connect('activate', self.reload_activate)
		item.set_image(Gtk.Image.new_from_stock('gtk-refresh', Gtk.IconSize.MENU))
		if not wms:
			item.set_sensitive(False)
		self.append(item)

		#Window Manager
		item = Gtk.ImageMenuItem('Select Window Manager')
		item.set_image(Gtk.Image.new_from_stock('gtk-index', Gtk.IconSize.MENU))
		submenu = WindowManagerMenu()
		item.set_submenu(submenu)
		if not wms:
			item.set_sensitive(False)
		self.append(item)

		#Compiz Options
		item = Gtk.ImageMenuItem('Compiz Options')
		item.set_image(Gtk.Image.new_from_stock('gtk-properties', Gtk.IconSize.MENU))
		submenu = CompizOptionMenu()
		item.set_submenu(submenu)
		if not options:
			item.set_sensitive(False)
		else:
			self.append(item)

		#Window Decorator
		item = Gtk.ImageMenuItem('Select Window Decorator')
		item.set_image(Gtk.Image.new_from_stock('gtk-select-color', Gtk.IconSize.MENU))
		submenu = CompizDecoratorMenu()
		item.set_submenu(submenu)
		if not decorators:
			item.set_sensitive(False)
		self.append(item)

		item = Gtk.SeparatorMenuItem()
		self.append(item)

		item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT)
		item.connect('activate', self.quit_activate)
		self.append(item)

	def show_menu(self, widget, button, time):
		self.show_all()
		self.popup(None, None, None, Gtk.StatusIcon.position_menu, button, time)

	def reload_activate(self, widget):
		wms.restart()

	def quit_activate(self, widget):
		Gtk.main_quit()

class ApplicationItem(Gtk.ImageMenuItem):

	def __init__(self, app):
		Gtk.ImageMenuItem.__init__(self, apps[app].label)

		self.app = app
		if app not in apps:
			self.set_sensitive(False)
		self.connect('activate', self.activate)

	def activate(self, widget):
		apps[self.app].launch()

class WindowManagerItem(Gtk.RadioMenuItem):

	def __init__(self, wm, group):
		Gtk.RadioMenuItem.__init__(self, label=' %s' %wms[wm].label, group=group)

		self.wm = wm
		if wms.active == wm:
			self.set_active(True)
		self.connect('activate', self.activate)

	def activate(self, widget):
		if widget.get_active():
			wms.active = self.wm
			wms.start()

class WindowManagerMenu(Gtk.Menu):

	def __init__(self):
		Gtk.Menu.__init__(self)

		prev = None
		for wm in wms.ordered_list:
			item = WindowManagerItem(wm, prev)
			self.append(item)
			prev = item

class CompizOptionItem(Gtk.CheckMenuItem):

	def __init__(self, option):
		Gtk.CheckMenuItem.__init__(self, label=' %s' %options[option].label)

		self.option = option
		self.set_active(options[option].enabled)
		if not options[option].sensitive:
			self.set_sensitive(False)
		self.connect('activate', self.activate)

	def activate(self, widget):
		options[self.option].enabled = widget.get_active()
		if wms.active == 'compiz':
			wms.start()

class CompizOptionMenu(Gtk.Menu):

	def __init__(self):
		Gtk.Menu.__init__(self)

		for option in options:
			item = CompizOptionItem(option)
			self.append(item)

class CompizDecoratorItem(Gtk.RadioMenuItem):

	def __init__(self, decorator, group):
		Gtk.RadioMenuItem.__init__(self, label=' %s' %decorators[decorator].label, group=group)

		self.decorator = decorator
		if decorators.active == decorator:
			self.set_active(True)
		self.connect('activate', self.activate)

	def activate(self, widget):
		if widget.get_active():
			decorators[self.decorator].kill_others()
			time.sleep(0.5)
			decorators.active = self.decorator

class CompizDecoratorMenu(Gtk.Menu):

	def __init__(self):
		Gtk.Menu.__init__(self)

		prev = None
		for decorator in decorators:
			item = CompizDecoratorItem(decorator, prev)
			item.set_name(str(decorator))
			self.append(item)
			prev = item

icon = Gtk.StatusIcon.new_from_icon_name('fusion-icon')
icon.set_tooltip_text('Compiz Fusion Icon')
menu = TrayMenu()
icon.connect('popup-menu', menu.show_menu)

# active wm (possibly) starts here
init()
Gtk.main()
