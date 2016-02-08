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
# Original copyright 2007 Christopher Williams <christopherw@verizon.net>
# Author(s): crdlb, nesl247, raveit65

import subprocess, signal, os

# avoid zombies
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

def run(command, mode='spawn', quiet=False, env=None):
	'Simple wrapper for the subprocess module. Supported modes: spawn, call, and output'

	try:
		if mode == 'spawn':
			if not quiet:
				popen_object = subprocess.Popen(command)
			else:
				popen_object = subprocess.Popen(command, stdout=open(os.devnull, 'w'))

			return popen_object

		elif mode == 'call':
			# restore normal child handling
			signal.signal(signal.SIGCHLD, signal.SIG_DFL)
			if not quiet:
				exitcode = subprocess.call(command, stderr=subprocess.PIPE)
			else:
				exitcode = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			# turn zombie protection back on
			signal.signal(signal.SIGCHLD, signal.SIG_IGN)

			return exitcode

		elif mode == 'output':
			signal.signal(signal.SIGCHLD, signal.SIG_DFL)
			if not env:
				output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=open(os.devnull, 'w')).communicate()[0]
			else:
				output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), env=env).communicate()[0]

			signal.signal(signal.SIGCHLD, signal.SIG_IGN)

			return output

	except OSError:
		print(' * execution of "' + ' '.join(command) + '" failed')
		return None
