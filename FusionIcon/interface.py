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
# Author(s): crdlb, nesl247
#
# Copyright 2007 Christopher Williams <christopherw@verizon.net> 

import sys
from util import env
import start

interfaces={
	'gtk': 'GTK',
	'qt4': 'Qt4',
	'qt3': 'Qt3',
}

def import_interface(interface):	
	try:
		if interface in interfaces:
			print ' * Using the', interfaces[interface], 'Interface'
			__import__('FusionIcon.interface_%s' %interface)
		
		else:
			print ' *** Error: "%s" interface is invalid, this should not happen' %interface
			raise SystemExit

	except ImportError, e:
		if [i for i in interfaces if 'interface_%s' %i in str(e)]:
			print ' * Interface not installed'
		else:
			print ' *', e

		#doesn't work so remove it from the dict
		del interfaces[interface]
		if interfaces:
			print ' ... Trying another interface'
			choose_interface()
		else:
			print ' *** Error: All interfaces failed, aborting!'
			raise SystemExit

def choose_interface(try_first=None):

	chosen_interface = None

	# handle explicit choice first
	if try_first:
		if try_first in interfaces:
			chosen_interface = try_first
		else:
			raise SystemExit, ' *** Error: No such interface: %s' %try_first
	else:

# gtk for everybody for now
		# use qt for kde; gtk for everything else:
#		if 'qt4' in interfaces and env.desktop == 'kde':
#			chosen_interface = 'qt4'

#		elif 'qt3' in interfaces and env.desktop == 'kde':
#			chosen_interface = 'qt3'

		if 'gtk' in interfaces:
			chosen_interface = 'gtk'

		# try qt* for non-kde:
		elif 'qt4' in interfaces:
			chosen_interface = 'qt4'
		elif 'qt3' in interfaces:
			chosen_interface = 'qt3'

		# interfaces is empty
		else:
			raise SystemExit, ' *** no available interfaces, this should not happen'

	import_interface(chosen_interface)

