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
# You should have received a copy of the GNU General Publaic License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Original copyright 2007 Christopher Williams <christopherw@verizon.net> 
# Author(s): crdlb, kozec, raveit65

import os

mesa_libgl_locations = (
	# ubuntu
	'/usr/lib/fglrx/libGL.so.1.2.xlibmesa',
	'/usr/lib/nvidia/libGL.so.1.2.xlibmesa',
	# gentoo
	'/usr/lib/opengl/xorg-x11/lib/libGL.so.1.2',
	# archlinux
	'/opt/mesa-xgl/lib/libGL.so.1.2',
	'/lib/mesa/libGL.so.1.2',
	# debian
	'/usr/lib/fglrx/diversions/libGL.so.1.2',
	'/usr/share/nvidia-glx/diversions/libGL.so.1.2',
)

compiz_args = ['ccp', '--replace', '--sm-disable', '--ignore-desktop-hints']

config_home = os.environ.get('XDG_CONFIG_HOME',
			os.path.join(os.environ['HOME'], '.config'))

config_folder = os.path.join(config_home, 'compiz')

config_file = os.path.join(config_folder, 'fusion-icon')

#app
#	base command, full command line
#	label

apps = {
	'ccsm':
		('ccsm', ['ccsm'],
		'Settings Manager'),
	'emerald theme manager':
		('emerald-theme-manager', ['emerald-theme-manager'],
		'Emerald Theme Manager'),
}

#wm
#	base command, full command line
#	label, desktop, special flags, command to run before replacing

wms = {
	'marco':
		('marco', ['marco', '--replace'],
		 'Marco', 'mate', None, None,),

	'metacity':
		('metacity', ['metacity', '--replace'],
		 'Metacity', 'gnome', None, None,),

	'mutter':
		('mutter', ['mutter', '--replace'],
		 'Mutter', 'gnome', None, None,),

	'kwin':
		('kwin_x11', ['kwin_x11', '--replace'],
		 'KWin', 'kde', None, None),

	'kwin4':
		('kwin', ['kwin', '--replace'],
		 'KWin4', 'kde', None, None),

	'xfwm4':
		('xfwm4', ['xfwm4', '--replace'],
		 'Xfwm4', 'xfce', None, None),

	'openbox':
		('openbox', ['openbox', '--replace'],
		 'Openbox', None, None, None),

	'blackbox':
		('blackbox', ['blackbox', '--replace'],
		 'Blackbox', None, None, None),

	'fvwm':
		('fvwm', ['fvwm', '--replace'],
		 'FVWM', None, None, None),

	'icewm':
		('icewm', ['icewm', '--replace'],
		 'IceWM', None, None, None),

}

#decorator
#	base command, full command line,
#	label, desktop environment

decorators = {
	'emerald':
		('emerald', 'emerald --replace',
		 'Emerald', None),

	'gwd':
		('gtk-window-decorator', 'gtk-window-decorator --replace',
		 'GTK+ Window Decorator', 'mate'),
}

#option:
#	(unused), switch,
#	label

options = {
	'indirect rendering':
		(None, '--indirect-rendering', 'Indirect Rendering'),

	'loose binding':
		(None, '--loose-binding', 'Loose Binding'),
}
