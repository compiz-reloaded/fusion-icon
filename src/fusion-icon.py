#!/usr/bin/env python
# Compiz Fusion Icon
import os, sys, time

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
	sys.exit(0)

def reset():
	#cut-and-pasted from libfusionicon to avoid a full load for --reset
	if os.environ.has_key('XDG_CONFIG_HOME'):
		config_folder = os.environ['XDG_CONFIG_HOME']
	else:	
		config_folder = os.path.join(os.environ['HOME'], '.config')

	config_file = os.path.join(config_folder, 'fusion-icon')

	print '* Configuration file (' + config_file + ') being reset'

	try:
		if os.path.exists(config_file):
			config_backup = os.path.join(config_folder, 'fusion-icon.backup.' + str(int(time.time())))
			os.rename(config_file, config_backup)
			print '... backed up to:', config_backup
		else:
			print '... no configuration found'
		print '* Configuration reset'

	except:
		print '* Error: configuration reset failed'
		sys.exit(1)

	sys.exit(0)
	
interfaces={'gtk':('GTK', ('pygtk', 'interface_gtk')),
			'qt4':('Qt4', ('PyQt4', 'interface_qt4')),
			'qt3':('Qt3', ('qt', 'ctypes', 'interface_qt3'))}

def import_interface(interface):	
	try:
		print '* Using the ' + interfaces[interface][0] + ' Interface'
		for module in interfaces[interface][1]:
			exec('import ' + module)

	except ImportError, e:
		print '*', e
		#doesn't work so remove it from the dict
		del interfaces[interface]
		print '... Trying anonther interface'
		choose_interface()

def choose_interface():
	#handle explicit arguments first:
	if interfaces.has_key('gtk') and '--gtk' in args: interface = 'gtk'	
	elif interfaces.has_key('qt4') and '--qt4' in args: interface = 'qt4'
	elif interfaces.has_key('qt3') and '--qt3' in args: interface = 'qt3'
	
	#use qt* for kde; gtk for everything else:
	elif interfaces.has_key('qt4') and kde: interface = 'qt4'
	elif interfaces.has_key('qt3') and kde: interface = 'qt3'
	elif interfaces.has_key('gtk'): interface = 'gtk'
	
	#try qt* for non-kde:
	elif interfaces.has_key('qt4'): interface = 'qt4'
	elif interfaces.has_key('qt3'): interface = 'qt3'
	
	#interfaces is empty
	else:
		print '* Error: All interfaces failed, aborting!'
		sys.exit(1)

	import_interface(interface)	

#Abbreviate for readability
args = sys.argv

## Detect and run args
# If we're running --help or --reset, don't progress past it
if '--help' in args or '-h' in args:
	help()

if '--reset' in args:
	reset()

#If there is a positive integer following '--sleep' in argv, sleep for that time
try:
	if '--sleep' in args and int(args[args.index('--sleep') + 1]) > 0:
		time.sleep(int(args[args.index('--sleep') + 1]))

except IOError:
	print '* Error: invalid sleep amount'
	sys.exit(1)

# Remove the need to import libfusionicon.py
# We'll detect kde right here
kde = False
if os.system('pgrep gnome-session 1>/dev/null') != 0 and os.system('pgrep xfce4-session 1>/dev/null') != 0:
	if os.system('pgrep kdeinit 1>/dev/null') == 0 or os.system('pgrep startkde 1>/dev/null') == 0:
		kde = True

# Use what's specified, or use autodetection
choose_interface()

