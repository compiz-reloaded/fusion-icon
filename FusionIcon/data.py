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
# You should have received a copy of the GNU General Publaic License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): crdlb
# Copyright 2007 Christopher Williams <christopherw@verizon.net> 

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

compiz_args = ['--replace', '--sm-disable', '--ignore-desktop-hints', 'ccp']

config_home = os.environ.get('XDG_CONFIG_HOME',
			os.path.join(os.environ['HOME'], '.config'))

config_folder = os.path.join(config_home, 'compiz')

config_file = os.path.join(config_folder, 'fusion-icon')

# Key:
#  identifier (for wms, this is what gets written to the config file)
# Value:
#  O - base command (for wms and decorators), config file option name
#  1 - full command, actual compiz argument
#  2 - display name
#  3 - desktop environment for which it should be the fallback/default
#  4 - list of extra properties:
#          noreplace: lacks working --replace switch
#  5 - Extra command to run before killing

apps = {
	'ccsm':
		('ccsm', ['ccsm'],
		'Settings Manager'),
	'emerald theme manager':
		('emerald-theme-manager', ['emerald-theme-manager'],
		'Emerald Theme Manager'),
}

wms = {
	'metacity':
		('metacity', ['metacity', '--replace'],
		 'Metacity', 'gnome', None, None,),

	'kwin':
		('kwin', ['kwin', '--replace'],
		 'KWin', 'kde', None, ['dcop', 'kwin', 'KWinInterface', 'stopKompmgr']),

	'xfwm4':
		('xfwm4', ['xfwm4'],
		 'Xfwm4', 'xfce4', ['noreplace'], ['killall', 'xfwm4']),

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

decorators = {
	'emerald':
		('emerald', 'emerald --replace', 
		 'Emerald', None),

	'gwd': 
		('gtk-window-decorator', 'gtk-window-decorator --replace', 
		 'GTK Window Decorator', 'gnome'),

	'kwd':
		('kde-window-decorator', 'kde-window-decorator --replace',
		 'KDE Window Decorator', 'kde'),
}

options = {
	'indirect rendering':
		(None, '--indirect-rendering', 'Indirect Rendering'),

	'loose binding': 
		(None, '--loose-binding', 'Loose Binding'),
}

