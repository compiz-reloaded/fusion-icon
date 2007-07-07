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
		
interfaces={'gtk':('GTK', ('pygtk', 'interface_gtk')),
	'qt4':('Qt4', ('PyQt4', 'interface_qt4')),
	'qt3':('Qt3', ('qt', 'ctypes', 'interface_qt3'))}

def int_import(interface):
	try:
		print '* Using the ' + interfaces[interface][0] + ' Interface'
		for x in interfaces[interface][1]:
			exec('import ' + x)
			
	except ImportError:
		print '* Error: failed to import: ' + "".join(interfaces[interface][1])
		sys.exit(1)

## Detect and run args
# If we're running --help or --reset, don't progress past it
if '--help' in sys.argv or '-h' in sys.argv	:
	help()

if '--reset' in sys.argv:
	reset()
	
# Remove the need to import libfusionicon.py
# We'll detect kde right here
kde = False
if os.system('pgrep kdesktop 1>/dev/null') == 0 or os.system('pgrep startkde 1>/dev/null') == 0:
	kde = True

# Use what's specified, or use autodetection
if '--qt3' in sys.argv:
	int_import('qt3')

else:
	if (kde and not '--gtk' in sys.argv) or '--qt4' in sys.argv:
		int_import('qt4')	
	
	else:
		int_import('gtk')
