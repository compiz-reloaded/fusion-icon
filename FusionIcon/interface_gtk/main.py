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
    raise ImportError, 'PyGtk 2.10.0 or later required'

import time
from FusionIcon.start import wms, apps, options, decorators, init

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

def show_menu(widget, button, time, menu):
	menu.show_all()
	menu.popup(None, None, gtk.status_icon_position_menu, button, time, icon)

def reload_activate(widget):
	wms.restart()

def quit_activate(widget):
	gtk.main_quit()

menu = gtk.Menu()

#CCSM
item = ApplicationItem('ccsm')
item.set_image(gtk.image_new_from_stock('gtk-preferences', gtk.ICON_SIZE_MENU))
menu.append(item)

#Emerald Theme Manager
item = ApplicationItem('emerald theme manager')
if 'emerald theme manager' in apps:
	item.set_image(gtk.image_new_from_icon_name('emerald-theme-manager-icon', gtk.ICON_SIZE_MENU))
menu.append(item)

item = gtk.SeparatorMenuItem()
menu.append(item)

#Reload
item = gtk.ImageMenuItem('Reload Window Manager')
item.connect('activate', reload_activate)
item.set_image(gtk.image_new_from_stock('gtk-refresh', gtk.ICON_SIZE_MENU))
if not wms:
	item.set_sensitive(False)
menu.append(item)

#Window Manager
item = gtk.ImageMenuItem('Select Window Manager')
item.set_image(gtk.image_new_from_stock('gtk-index', gtk.ICON_SIZE_MENU))
submenu = gtk.Menu()
first = True
for wm in wms.ordered_list:
	if first:
		first_item = WindowManagerItem(wm)
		submenu.append(first_item)
		first = False
	else:
		sitem = WindowManagerItem(wm, first_item)
		submenu.append(sitem)
item.set_submenu(submenu)
if not wms:
	item.set_sensitive(False)
menu.append(item)

#Compiz Options
item = gtk.ImageMenuItem('Compiz Options')
item.set_image(gtk.image_new_from_stock('gtk-properties', gtk.ICON_SIZE_MENU))
submenu = gtk.Menu()
for option in options:
	sitem = CompizOptionItem(option)
	submenu.append(sitem)
item.set_submenu(submenu)
if not options:
	item.set_sensitive(False)
menu.append(item)

#Window Decorator
item = gtk.ImageMenuItem('Select Window Decorator')
item.set_image(gtk.image_new_from_stock('gtk-select-color', gtk.ICON_SIZE_MENU))
submenu = gtk.Menu()
first = True
for decorator in decorators:
	if first:
		first_item = CompizDecoratorItem(decorator)
		submenu.append(first_item)
		first = False
	else:
		sitem = CompizDecoratorItem(decorator, first_item)
		submenu.append(sitem)
item.set_submenu(submenu)
if not decorators:
	item.set_sensitive(False)
menu.append(item)

item = gtk.SeparatorMenuItem()
menu.append(item)

item = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
item.connect('activate', quit_activate)
menu.append(item)

icon = gtk.status_icon_new_from_icon_name('fusion-icon')
icon.set_tooltip('Compiz Fusion Icon')
icon.connect('popup-menu', show_menu, menu)

# active wm (possibly) starts here
init()
gtk.main()

