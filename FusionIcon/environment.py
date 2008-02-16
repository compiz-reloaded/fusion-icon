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

import os
from execute import run

tfp = 'GLX_EXT_texture_from_pixmap'
GDSID = 'GNOME_DESKTOP_SESSION_ID'

class Environment:

	'''Detects properties of the enviroment, and provides a set() method that uses this information to export environment variables needed to start compiz.'''
	

	def __init__(self):

		'''desktop: current desktop enviroment used to choose interface, fallback wm, and default decorator
	
failsafe: boolean, True if in a failsafe session, currently only supports gnome failsafe mode.

glxinfo: output of glxinfo command

indirect_glxinfo: output of glxinfo with LIBGL_ALWAYS_INDIRECT

xvinfo: output of xvinfo

glx_vendor: 'client glx vendor:' usually one of SGI (for mesa-based drivers), NVIDIA Corporation, or ATI.

tfp: 'direct' if texture_from_pixmap is present with direct rendering (implying presence with indirect as well), 'indirect' if only present with indirect context, False if not present at all

Xgl: True in Xgl'''

		# Check gnome- and kde-specific vars, then try generic 'DESKTOP_SESSION'
		if GDSID in os.environ:
			self.desktop = 'gnome'

		elif 'KDE_FULL_SESSION' in os.environ: 
			self.desktop = 'kde'

		else:
			self.desktop = os.environ.get('DESKTOP_SESSION', 'unknown')

		self.failsafe = False
		if self.desktop == 'gnome' and GDSID in os.environ and os.environ[GDSID] == 'failsafe':
			self.failsafe = True
		
		if self.failsafe:
			failsafe_str = 'failsafe '
		else:
			failsafe_str = ''

		# hack to eliminate inconsistency
		if self.desktop == 'kde4':
			self.desktop = 'kde'


		print ' * Detected Session: %s%s' %(failsafe_str, self.desktop)


		## Save the output of glxinfo and xvinfo for later use:

		# don't try to run glxinfo unless it's installed
		if run(['which', 'glxinfo'], 'call', quiet=True) == 0:
			self.glxinfo = run('glxinfo', 'output')
		else:
			raise SystemExit, ' * Error: glxinfo not installed!'

		# make a temp environment 
		indirect_environ = os.environ.copy()
		indirect_environ['LIBGL_ALWAYS_INDIRECT'] = '1'
		self.indirect_glxinfo = run('glxinfo', 'output', env=indirect_environ)

		if run(['which', 'xvinfo'], 'call', quiet=True) == 0:
			self.xvinfo = run('xvinfo', 'output')
		else:
			raise SystemExit, ' * Error: xvinfo not installed!'

		self.glx_vendor = None
		line = [l for l in self.glxinfo.splitlines() if 'client glx vendor string:' in l]
		if line:
			self.glx_vendor = ' '.join(line[0].split()[4:])

		## Texture From Pixmap / Indirect
		self.tfp = False
		if self.glxinfo.count(tfp) < 3:
			if self.indirect_glxinfo.count(tfp) == 3:
				self.tfp = 'indirect'
		else:
			self.tfp = 'direct'

		## Xgl
		if 'Xgl' in self.xvinfo:
			self.Xgl = True

		else:
			self.Xgl = False

	def set(self):

		'''Trigger all environment checks'''

		# Check for Intel and export INTEL_BATCH
		if 'Intel' in self.glxinfo:
			print ' * Intel detected, exporting: INTEL_BATCH=1'
			os.environ['INTEL_BATCH'] = '1'

		# Check TFP and export LIBGL_ALWAYS_INDIRECT if needed
		if self.tfp != 'direct':
			print ' * No %s with direct rendering context' %tfp
			if self.tfp == 'indirect':
				print ' ... present with indirect rendering, exporting: LIBGL_ALWAYS_INDIRECT=1'
				os.environ['LIBGL_ALWAYS_INDIRECT'] = '1'
			else:
				# If using Xgl with a proprietary driver, exports LD_PRELOAD=<mesa libGL>
				if self.Xgl and self.glx_vendor != 'SGI':
					print ' * Non-mesa driver on Xgl detected'
					from data import mesa_libgl_locations
					location = [l for l in mesa_libgl_locations if os.path.exists(l)]
					if location:
						print ' ... exporting: LD_PRELOAD=%s' %location[0]
						os.environ['LD_PRELOAD'] = location[0]
						if run(['glxinfo'], 'output').count(tfp) >= 3:
							self.tfp = 'direct'
						
					else:
						# kindly let the user know... but don't abort (maybe it will work :> )
						print ' ... no mesa libGL found for preloading, this may not work!'
				else:
					print ' ... nor with indirect rendering, this isn\'t going to work!'

		# Check for nvidia on Xorg
		if not self.Xgl and self.glx_vendor == 'NVIDIA Corporation':
			print ' * NVIDIA on Xorg detected, exporting: __GL_YIELD=NOTHING'
			os.environ['__GL_YIELD'] = 'NOTHING'

env = Environment()

