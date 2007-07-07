#!/usr/bin/env python
# Compiz Fusion Icon
from os import system, environ, path, rename
from sys import exit, argv
from time import time, sleep

def help():
	print 'Usage: fusion-icon [action|interface]'
	print
	print '  --help	Display this text'
	print '  --reset	Remove fusion-icon configuration file'
	print '  --sleep n	Sleep for n seconds before launching'
	print
	print 'Interfaces:'
	print '  --gtk		Use the pygtk 2.10 interface'
	print '  --qt3		Use the PyQt3 interface'
	print '  --qt4		Use the PyQt4 interface'
	exit(0)

def reset():
	#cut-and-pasted from libfusionicon to avoid a full load for --reset
	config_folder = environ.get('XDG_CONFIG_HOME', path.join(environ.get('HOME'), '.config'))
	config_file = path.join(config_folder, 'fusion-icon')
	print '* Configuration file (' + config_file + ') being reset'

	try:
		if path.exists(config_file):
			config_backup = path.join(config_folder, 'fusion-icon.backup.' + str(int(time())))
			rename(config_file, config_backup)
			print '... backed up to:', config_backup
		else:
			print '... no configuration found'
		print '* Configuration reset'

	except:
		print '* Error: configuration reset failed'
		exit(1)

	exit(0)
	
interfaces={'gtk':('GTK', ('pygtk', 'interface_gtk')),
	'qt4':('Qt4', ('PyQt4', 'interface_qt4')),
	'qt3':('Qt3', ('qt', 'ctypes', 'interface_qt3'))}

def int_import(interface):
	try:
		print '* Using the ' + interfaces[interface][0] + ' Interface'
		for module in interfaces[interface][1]:
			exec('import ' + module)

	except ImportError:
		print '* Error: failed to import: ' + ', '.join(interfaces[interface][1])
		exit(1)

## Detect and run args
# If we're running --help or --reset, don't progress past it
if '--help' in argv or '-h' in argv:
	help()

if '--reset' in argv:
	reset()

#If there is a positive integer following '--sleep' in argv, sleep for that time
try:
	if '--sleep' in argv and int(argv[argv.index('--sleep') + 1]) > 0:
		sleep(int(argv[argv.index('--sleep') + 1]))

except ValueError, IOError:
	print '* Error: invalid sleep amount'
	exit(1)

# Remove the need to import libfusionicon.py
# We'll detect kde right here
kde = False
if system('pgrep kdeinit 1>/dev/null') == 0 or system('pgrep startkde 1>/dev/null') == 0:
	kde = True

# Use what's specified, or use autodetection
if '--qt3' in argv:
	int_import('qt3')

else:
	if (kde and not '--gtk' in argv) or '--qt4' in argv:
		int_import('qt4')

	else:
		int_import('gtk')
