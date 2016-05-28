# -*- python -*-
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

import sys, os
from FusionIcon.util import env
from FusionIcon import start

interfaces={
	'qt': 'Qt',
	'gtk': 'GTK+',
}

def import_interface(interface):
	try:
		if interface in interfaces:
			print(' * Using the ' + interfaces[interface] + ' Interface')
			__import__('FusionIcon.interface_' + interface)

		else:
			print(' *** Error: "' + interface + '" interface is invalid, this should not happen')
			raise SystemExit

	except ImportError as e:
		if [i for i in interfaces if 'interface_' + i in str(e)]:
			print(' * Interface not installed')
		else:
			print(' * ' + str(e))

		#doesn't work so remove it from the dict
		del interfaces[interface]
		if interfaces:
			print(' ... Trying another interface')
			choose_interface()
		else:
			print(' *** Error: All interfaces failed, aborting!')
			raise SystemExit

def choose_interface(try_first=None):

	chosen_interface = None

	# handle explicit choice first
	if try_first:
		if try_first in interfaces:
			chosen_interface = try_first
		else:
			raise SystemExit(' *** Error: No such interface: ' + try_first)
	else:

		# use qt for kde and lxqt; gtk for everything else:
		if os.getenv('FUSION_ICON_INTERFACE') in interfaces:
			chosen_interface = os.getenv('FUSION_ICON_INTERFACE')
		elif 'qt' in interfaces and env.desktop in ('kde', 'lxqt'):
			chosen_interface = 'qt'
		elif 'gtk' in interfaces:
			chosen_interface = 'gtk'
		elif 'qt' in interfaces:
			chosen_interface = 'qt'
		# interfaces is empty
		else:
			raise SystemExit(' *** no available interfaces, this should not happen')

	import_interface(chosen_interface)
