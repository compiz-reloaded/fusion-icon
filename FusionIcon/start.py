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
# Original copyright 2007 Christopher Williams <christopherw@verizon.net>
# Author(s): crdlb, nesl247, raveit65

from parser import options as parser_options
from util import env, config, apps, options, wms, decorators

def init():
	'Final start function, should be called once when fusion-icon starts'

	if not parser_options.no_start:
		# Do not restart the wm if it's already running
		if wms.active == wms.active == wms.old != 'compiz':
			#always restart compiz since we can't know compiz was started correctly
			print(' * ' + wms[wms.active].label + ' is already running')
		else:
			print(' * Starting ' + wms[wms.active].label)
			wms.start()

config.check()

# Make some changes

if not parser_options.force_compiz:
	if wms.active not in wms:
		print(' * "' + wms.active + '" not installed')
		if wms.fallback:
			print(' ... setting to fallback...')
		else:
			print(' ... No fallback window manager chosen')
		wms.active = wms.fallback

elif 'compiz' in wms:
	wms.active = 'compiz'

else:
	raise SystemExit, ' *** Error: "--force-compiz" used and compiz not installed!'

# Set True if using Xorg AIGLX since the '--indirect-rendering' option has no effect in that situation. 
env.set()
if env.tfp == 'indirect' and 'indirect rendering' in options:
	options['indirect rendering'].sensitive = False
	if not options['indirect rendering'].enabled:
		options['indirect rendering'].enabled = True
