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
# Author(s): crdlb
# Copyright 2007 Christopher Williams <christopherw@verizon.net> 

from optparse import OptionParser, OptionGroup

parser = OptionParser(usage='usage: %prog [options|action]', version='%prog-0.0.0')

parser.add_option('--reset', action='store_true', dest='reset',
	help='remove configuration file and exit')

parser.add_option('-s', '--sleep', type='int', dest='seconds',
	help='Sleep before launching')

parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
	help='Print extra output')

interface_group = OptionGroup(parser, 'Interface Options')

interface_group.add_option('-i', '--interface', dest='interface',
	help='Try a certain interface first')

interface_group.add_option('-u', '--no-interface', action='store_true', dest='no_interface',
	help='Do not use any interface')

parser.add_option_group(interface_group)

startup_group = OptionGroup(parser, 'Startup Options')

startup_group.add_option('-f', '--force-compiz', action='store_true', dest='force_compiz',
	help='Start compiz regardless of environment or configuration')

startup_group.add_option('-n', '--no-start', action='store_true', dest='no_start',
	help='Run, but do not start a window manager')

parser.add_option_group(startup_group)

options, args = parser.parse_args()

# fusion-icon accepts no arguments
if args:
	parser.error('no such argument: %s' %args[0])

