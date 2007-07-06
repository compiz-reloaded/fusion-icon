#!/usr/bin/env python
# Compiz Fusion Icon

import os, sys, time

def help():
	print 'Usage: fusion-icon [action|interface]'
	print
	print '  --help     Display this text'
	print '  --reset    Remove fusion-icon configuration file'
	print
	print 'Interfaces:'
	print '  --gtk      Use the pygtk 2.10 interface'
	print '  --qt3      Use the PyQt3 interface (currently not installed by default)'
	print '  --qt4      Use the PyQt4 interface'
	sys.exit(0)

def reset():
	#cut-and-pasted from libfusionicon to avoid a full load for --reset 
	config_folder = environ.get('XDG_CONFIG_HOME', path.join(environ.get('HOME'), '.config'))  
	config_file = path.join(config_folder, 'fusion-icon')
	print '* Configuration file (' + config_file + ') being reset'
	try:
		if path.exists(config_file):
			config_backup = path.join(config_folder, 'fusion-icon.backup.' + str(int(time.time())))
			rename(config_file, config_backup)
			print '... backed up to:', config_backup
		print '* Configuration reset'
		sys.exit(0)
		
	except:
		print '* Error: configuration reset failed'
			
def import_gtk(die_on_error=False):
	try:
		print '* Using the GTK Interface'
		import pygtk, interface_gtk
	
	except ImportError:
		print '* Error: failed to import pygtk'
		if die_on_error:
			sys.exit(1)
		
def import_qt4(die_on_error=False):
	try:
		print '* Using the Qt4 Interface'
		import PyQt4, interface_qt4
		
	except ImportError:
		print '* Error: failed to import PyQt4'
		if die_on_error:
			sys.exit(1)
			
def import_qt3(die_on_error=False):
	try:
		print '* Using the Qt3 Interface'
		import qt, ctypes, interface_qt3

	except ImportError:
		print '* Error: failed to import PyQt3'
		if die_on_error:
			sys.exit(1)

## Detect and run args
# If we're running --help or --reset, don't progress past it
if '--help' in sys.argv or '-h' in sys.argv	:
	help()

if '--reset' in sys.argv:
	reset()
	
# Passed help and reset, import libfusionicon
from libfusionicon import *

# Passed --reset, so either use what's specified, or use autodetection
interface = ''
if '--gtk' in sys.argv:
	interface = 'gtk'
elif '--qt4' in sys.argv:
	interface = 'qt4'
elif '--qt3' in sys.argv:
	interface = 'qt3'

if interface == '':
	if gnome or xfce4:
		interface = 'gtk'
	elif kde:
		interface = 'qt4'
	else:
		interface = 'gtk'

if interface == 'gtk':
	import_gtk(True)	
elif interface == 'qt4':
	import_qt4(True)
elif interface == 'qt3':
	import_qt3(True)
else:
	print '*** Failed autodetection, you must be using an unsupported DE. (Gnome, KDE, XFCE4 are supported)'
	sys.exit(1)
