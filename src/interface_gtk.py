#!/usr/bin/env python
# Author(s): crdlb
import pygtk
pygtk.require('2.0')
import gtk
from libfusionicon import *
import time

# Compiz-Manager Menu Functions
def popup_menu(widget, button, time, data=None):
	data.show_all()
	data.popup(None, None, gtk.status_icon_position_menu, 3, time, icon)

def configure_menu_activate(widget):
	subprocess.Popen(['ccsm'])

def etm_menu_activate(widget):
	subprocess.Popen(['emerald-theme-manager'])

def wm_activate(widget):
	print '* reloading window manager...'
	start_wm()

def compiz_menu_activate(widget):
	if compiz_wm.active and initialized:
		set_old_wm()
		set_setting('window manager', 'active wm', compiz)
		print '* switching to Compiz...'
		start_wm()
	
def kwin_menu_activate(widget):
	if kwin_wm.active and initialized:
		set_old_wm()
		set_setting('window manager', 'active wm', 'kwin')
		print '* switching to Kwin...'
		start_wm()

def metacity_menu_activate(widget):
	if metacity_wm.active and initialized:
		set_old_wm()
		set_setting('window manager', 'active wm', 'metacity')
		print '* switching to Metacity...'
		start_wm()

def xfwm4_menu_activate(widget):
	if xfwm4_wm.active and initialized:
		set_old_wm()
		set_setting('window manager', 'active wm', 'xfwm4')
		print '* switching to Xfwm4...'
		start_wm()

def emerald_menu_activate(widget):
	if initialized and emerald_decorator.active:
		active_wm = get_setting('window manager', 'active wm')
		if active_wm == compiz:
			os.system('killall gtk-window-decorator kde-window-decorator 2>/dev/null')
			time.sleep(1)
		set_decorator(emerald)

def kwd_menu_activate(widget):
	if initialized and kwd_decorator.active:
		if active_wm == compiz:
			os.system('killall emerald gtk-window-decorator 2>/dev/null')
			time.sleep(1)
		set_decorator(kwd)

def gwd_menu_activate(widget):
	if initialized and gwd_decorator.active:
		if active_wm == compiz:
			os.system('killall emerald kde-window-decorator 2>/dev/null')
			time.sleep(1)
		set_decorator(gwd)

def option_ir_activate(widget):
	if initialized:
		set_setting('compiz options','indirect rendering', int(option_ir.get_active()))
		print '* Setting option "Indirect Rendering" to', option_ir.get_active()
		if active_wm == compiz and initialized:
			start_compiz()
		
def option_lb_activate(widget):
	if initialized:
		set_setting('compiz options','loose binding', int(option_lb.get_active()))
		print '* Setting option "Loose Binding" to', option_lb.get_active()
		if active_wm == compiz:
			start_compiz()

def quit_menu_activate(widget):
	gtk.main_quit()

initialized = False
active_wm = get_setting('window manager', 'active wm')
### User Interface ###

# Window Manager
wm_menu = gtk.Menu()
compiz_wm = gtk.RadioMenuItem(label=' Compiz')
compiz_wm.connect('activate', compiz_menu_activate)
if active_wm == compiz:
	compiz_wm.set_active(True)
if compiz == '':
	compiz_wm.set_active(False)
	compiz_wm.set_sensitive(False)
wm_menu.append(compiz_wm)

if is_installed('kwin'):
	kwin_wm = gtk.RadioMenuItem(label=' Kwin')
	kwin_wm.set_group(compiz_wm)
	kwin_wm.connect('activate', kwin_menu_activate)
	if active_wm == 'kwin':
		kwin_wm.set_active(True)
	wm_menu.append(kwin_wm)

if is_installed('metacity'):
	metacity_wm = gtk.RadioMenuItem(label=' Metacity')
	metacity_wm.set_group(compiz_wm)
	metacity_wm.connect('activate', metacity_menu_activate)
	if active_wm == 'metacity':
		metacity_wm.set_active(True)
	wm_menu.append(metacity_wm)

if is_installed('xfwm4'):
	xfwm4_wm = gtk.RadioMenuItem(label=' Xfwm4')
	xfwm4_wm.set_group(compiz_wm)
	xfwm4_wm.connect('activate', xfwm4_menu_activate)
	if active_wm == 'xfwm4':
		xfwm4_wm.set_active(True)
	wm_menu.append(xfwm4_wm)

# Compiz Options
options_menu = gtk.Menu()
option_ir = gtk.CheckMenuItem(label=' Indirect Rendering')
option_ir.connect('activate', option_ir_activate)
option_ir.set_active(indirect_rendering)
if always_indirect:
	option_ir.set_sensitive(False)
options_menu.append(option_ir)

option_lb = gtk.CheckMenuItem(label=' Loose Binding')
option_lb.connect('activate', option_lb_activate)
option_lb.set_active(loose_binding)
options_menu.append(option_lb)

# Window Decorator
decorator_menu = gtk.Menu()
emerald_decorator = gtk.RadioMenuItem(label=' Emerald')
emerald_decorator.connect('activate', emerald_menu_activate)
if active_decorator == emerald:
	emerald_decorator.set_active(True)
if not is_installed('emerald'):
	emerald_decorator.set_active(False)
	emerald_decorator.set_sensitive(False)
decorator_menu.append(emerald_decorator)

if is_installed('gtk-window-decorator'):
	gwd_decorator = gtk.RadioMenuItem(label=' GTK Window Decorator')
	gwd_decorator.set_group(emerald_decorator)
	gwd_decorator.connect('activate', gwd_menu_activate)
	if active_decorator == gwd:
		gwd_decorator.set_active(True)
	decorator_menu.append(gwd_decorator)

if is_installed('kde-window-decorator'):
	kwd_decorator = gtk.RadioMenuItem(label=' KDE Window Decorator')
	kwd_decorator.set_group(emerald_decorator)
	kwd_decorator.connect('activate', kwd_menu_activate)
	if active_decorator == kwd:
		kwd_decorator.set_active(True)
	decorator_menu.append(kwd_decorator)

# Compiz-Manager Tray Menu
menu = gtk.Menu()
item = gtk.ImageMenuItem('Settings Manager')
img_sm = gtk.image_new_from_stock('gtk-preferences', gtk.ICON_SIZE_MENU)
item.set_image(img_sm)
item.connect('activate', configure_menu_activate)
menu.append(item)
item = gtk.ImageMenuItem('Emerald Theme Manager')
if not is_installed('emerald'):
	item.set_sensitive(False)
item.connect('activate', etm_menu_activate)
if is_installed('emerald'):
	img_etm = gtk.image_new_from_icon_name('emerald-theme-manager-icon', gtk.ICON_SIZE_MENU)
	item.set_image(img_etm)
menu.append(item)
item = gtk.SeparatorMenuItem()
menu.append(item)

# Window Manager Options
item = gtk.ImageMenuItem('Reload Window Manager')
item.connect('activate', wm_activate)
img_refresh = gtk.image_new_from_stock('gtk-refresh', gtk.ICON_SIZE_MENU)
item.set_image(img_refresh)
menu.append(item)
item = gtk.ImageMenuItem('Select Window Manager')
item.set_submenu(wm_menu)
img_wm = gtk.image_new_from_stock('gtk-index', gtk.ICON_SIZE_MENU)
item.set_image(img_wm)
menu.append(item)
item = gtk.ImageMenuItem('Compiz Options')
item.set_submenu(options_menu)
img_options = gtk.image_new_from_stock('gtk-properties', gtk.ICON_SIZE_MENU)
item.set_image(img_options)
menu.append(item)
item = gtk.ImageMenuItem('Select Window Decorator')
item.set_submenu(decorator_menu)
img_wd = gtk.image_new_from_stock('gtk-select-color', gtk.ICON_SIZE_MENU)
item.set_image(img_wd)
menu.append(item)

item = gtk.SeparatorMenuItem()
menu.append(item)
item = gtk.ImageMenuItem(stock_id=gtk.STOCK_QUIT)
item.connect('activate', quit_menu_activate)
menu.append(item)

# Compiz Fusion Icon
icon = gtk.status_icon_new_from_icon_name('fusion-icon')
icon.set_tooltip('Compiz Fusion Icon')
icon.connect('popup-menu', popup_menu, menu)

initialized = True
gtk.main()
