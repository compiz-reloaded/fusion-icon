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
	sys.exit()

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

	sys.exit()
	
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
		print '... Trying another interface'
		choose_interface()
	
	sys.exit()

def choose_interface():

	def has(interface):
		return interfaces.has_key(interface)

	#handle explicit arguments first:
	if has('gtk') and '--gtk' in args: interface = 'gtk'	
	elif has('qt4') and '--qt4' in args: interface = 'qt4'
	elif has('qt3') and '--qt3' in args: interface = 'qt3'
	
	#use qt* for kde; gtk for everything else:
	elif has('qt4') and desktop == 'kde': interface = 'qt4'
	elif has('qt3') and desktop == 'kde': interface = 'qt3'
	elif has('gtk'): interface = 'gtk'
	
	#try qt* for non-kde:
	elif has('qt4'): interface = 'qt4'
	elif has('qt3'): interface = 'qt3'
	
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

#If there is a positive integer following '--sleep' in args, sleep for that time
try:
	seconds = int(args[args.index('--sleep') + 1])
	if seconds > 0:
		time.sleep(seconds)
except:
	pass #don't fail, just move on...

# Remove the need to import libfusionicon.py
# We'll detect kde right here
if os.environ.has_key('KDE_FULL_SESSION'): desktop = 'kde'
elif os.environ.has_key('DESKTOP_SESSION'): desktop = os.environ['DESKTOP_SESSION']
else: desktop = ''

# Use what's specified, or use autodetection
choose_interface()

