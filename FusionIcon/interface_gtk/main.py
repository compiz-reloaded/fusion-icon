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
# Author(s): crdlb
# Copyright 2007 Christopher Williams <christopherw@verizon.net> 

import os
import gtk
if gtk.pygtk_version < (2,10,0):
	# raise an ImportError here to trigger the Except statement in interface.py
    raise ImportError, 'PyGtk 2.10.0 or later required'

import time
from FusionIcon.start import wms, apps, options, decorators, init

class TrayMenu(gtk.Menu):
	
	def __init__(self):
		gtk.Menu.__init__(self)

		#CCSM
		if 'ccsm' in apps:
			item = ApplicationItem('ccsm')
			item.set_image(gtk.image_new_from_stock('gtk-preferences', gtk.ICON_SIZE_MENU))
			self.append(item)

		#Emerald Theme Manager
		if 'emerald theme manager' in apps:
			item = ApplicationItem('emerald theme manager')
			item.set_image(gtk.image_new_from_icon_name('emerald-theme-manager-icon', gtk.ICON_SIZE_MENU))
			self.append(item)

		if 'ccsm' in apps or 'emerald theme manager' in apps:
			item = gtk.SeparatorMenuItem()
			self.append(item)

		#Reload
		item = gtk.ImageMenuItem('Reload Window Manager')
		item.connect('activate', self.reload_activate)
		item.set_image(gtk.image_new_from_stock('gtk-refresh', gtk.ICON_SIZE_MENU))
		if not wms:
			item.set_sensitive(False)
		self.append(item)

		#Window Manager
		item = gtk.ImageMenuItem('Select Window Manager')
		item.set_image(gtk.image_new_from_stock('gtk-index', gtk.ICON_SIZE_MENU))
		submenu = WindowManagerMenu()
		item.set_submenu(submenu)
		if not wms:
			item.set_sensitive(False)
		self.append(item)

		#Compiz Options
		item = gtk.ImageMenuItem('Compiz Options')
		item.set_image(gtk.image_new_from_stock('gtk-properties', gtk.ICON_SIZE_MENU))
		submenu = CompizOptionMenu()
		item.set_submenu(submenu)
		if not options:
			item.set_sensitive(False)
		self.append(item)

		#Window Decorator
		item = gtk.ImageMenuItem('Select Window Decorator')
		item.set_image(gtk.image_new_from_stock('gtk-select-color', gtk.ICON_SIZE_MENU))
		submenu = CompizDecoratorMenu()
		item.set_submenu(submenu)
		if not decorators:
			item.set_sensitive(False)
		self.append(item)

		item = gtk.SeparatorMenuItem()
		self.append(item)

		item = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
		item.connect('activate', self.quit_activate)
		self.append(item)

	def show_menu(self, widget, button, time):
		self.show_all()
		self.popup(None, None, gtk.status_icon_position_menu, button, time, icon)

	def reload_activate(self, widget):
		wms.restart()

	def quit_activate(self, widget):
		gtk.main_quit()

class ApplicationItem(gtk.ImageMenuItem):

	def __init__(self, app):
		gtk.ImageMenuItem.__init__(self, apps[app].label)

		self.app = app
		if app not in apps:
			self.set_sensitive(False)
		self.connect('activate', self.activate)

	def activate(self, widget):
		apps[self.app].launch()

class WindowManagerItem(gtk.RadioMenuItem):

	def __init__(self, wm, first_item=None):
		gtk.RadioMenuItem.__init__(self, label=' %s' %wms[wm].label)

		self.wm = wm
		if first_item:
			self.set_group(first_item)
		if wms.active == wm:
			self.set_active(True)
		self.connect('activate', self.activate)

	def activate(self, widget):
		if widget.get_active():
			wms.active = self.wm
			wms.start()

class WindowManagerMenu(gtk.Menu):

	def __init__(self):
		gtk.Menu.__init__(self)

		first = True
		for wm in wms.ordered_list:
			if first:
				first_item = WindowManagerItem(wm)
				self.append(first_item)
				first = False
			else:
				item = WindowManagerItem(wm, first_item)
				self.append(item)

class CompizOptionItem(gtk.CheckMenuItem):

	def __init__(self, option):
		gtk.CheckMenuItem.__init__(self, label=' %s' %options[option].label)

		self.option = option
		self.set_active(options[option].enabled)
		if not options[option].sensitive:
			self.set_sensitive(False)
		self.connect('activate', self.activate)

	def activate(self, widget):
		options[self.option].enabled = widget.get_active()
		if wms.active == 'compiz':
			wms.start()

class CompizOptionMenu(gtk.Menu):

	def __init__(self):
		gtk.Menu.__init__(self)

		for option in options:
			item = CompizOptionItem(option)
			self.append(item)

class CompizDecoratorItem(gtk.RadioMenuItem):

	def __init__(self, decorator, first_item=None):
		gtk.RadioMenuItem.__init__(self, label=' %s' %decorators[decorator].label)

		self.decorator = decorator
		if first_item:
			self.set_group(first_item)
		if decorators.active == decorator:
			self.set_active(True)
		self.connect('activate', self.activate)

	def activate(self, widget):
		if widget.get_active():
			decorators[self.decorator].kill_others()
			time.sleep(0.5)
			decorators.active = self.decorator

class CompizDecoratorMenu(gtk.Menu):

	def __init__(self):
		gtk.Menu.__init__(self)

		first = True
		for decorator in decorators:
			if first:
				first_item = CompizDecoratorItem(decorator)
				self.append(first_item)
				first = False
			else:
				item = CompizDecoratorItem(decorator, first_item)
				self.append(item)

icon = gtk.status_icon_new_from_icon_name('fusion-icon')
icon.set_tooltip('Compiz Fusion Icon')
menu = TrayMenu()
icon.connect('popup-menu', menu.show_menu)

# active wm (possibly) starts here
init()
gtk.main()

