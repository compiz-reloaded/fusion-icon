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
# Based on compiz-icon, Copyright 2007 Felix Bellanger <keeguon@gmail.com>
#
# Author(s): crdlb
# Copyright 2007 Christopher Williams <christopherw@verizon.net> 

import os, compizconfig, ConfigParser, time
import data as _data
from parser import options as parser_options
from environment import env
from execute import run
import subprocess, signal

def is_running(app):
	'Use pgrep to determine if an app is running'

	if run(['pgrep', app], 'call', quiet=True) == 0:
		return True


class Application(object):

	def __init__(self, name, apps, installed):

		self.name = name
		self.apps = apps

		self.base = installed.apps[name][0]
		self.command = installed.apps[name][1]
		self.label = installed.apps[name][2]

	def launch(self):
		print ' * Launching %s' %self.label
		run(self.command)

class Applications(dict):

	def __init__(self, installed):
		for app in installed.apps:
			self[app] = Application(app, self, installed)

class CompizOption(object):

	def __init__(self, name, options, installed, config):

		self.options = options
		self.config = config

		self.name = name
		self.switch = installed.options[name][1]
		self.label = installed.options[name][2]
		self.sensitive = True

	def __get(self):
		return self.config.getboolean('compiz options', self.name)

	def __set(self, value):
		print ' * Setting option %s to %s' %(self.label, value)
		self.config.set('compiz options', self.name, str(bool(value)).lower())
		self.config.write(open(self.config.config_file, 'w'))

	enabled = property(__get, __set)

class CompizOptions(dict):

	def __init__(self, installed, config):
		for option in installed.options:
			self[option] = CompizOption(option, self, installed, config)

class WindowManager(object):

	def __init__(self, name, wms, installed):

		self.wms = wms
		self.name = name
		self.base = installed.wms[name][0]
		self.command = installed.wms[name][1]
		self.label = installed.wms[name][2]
		self.desktop = installed.wms[name][3]
		if installed.wms[name][4]:
			self.flags = installed.wms[name][4]
		else:
			self.flags = []
		self.killcmd = installed.wms[name][5]

class WindowManagers(dict):

	def __init__(self, installed, config):

		self.config = config

		for wm in installed.wms:
			self[wm] = WindowManager(wm, self, installed)

		self.fallback = None
		wm = [w for w in self if self[w].desktop == env.desktop]
		if wm:
			self.fallback = wm[0]

		elif [w for w in self if w != 'compiz']:
			self.fallback = list([w for w in self if w != 'compiz'])[0]

		self.__set_old()

		self.ordered_list = []
		for wm in ('compiz', self.fallback):
			if wm in self:
				self.ordered_list.append(wm)
		self.ordered_list.extend([wm for wm in self if wm not in self.ordered_list])
	
	def __get(self):
		return self.config.get('window manager', 'active wm')

	def __set(self, value):

		if value in wms:
			print ' * Setting window manager to', wms[value].label
		elif not value:
			print ' * Setting window manager to empty value'

		self.config.set('window manager', 'active wm', str(value))
		self.config.write(open(self.config.config_file, 'w'))

	def __set_old(self):
		
		self.old = None
		running_wm = [wm for wm in self if is_running(wm)]
		if running_wm:
			# not perfect, but good enough
			self.old = running_wm[0]

	def start(self):
		'Start the active window manager'
		
		self.__set_old()

		if self.active == 'compiz' and self.old and self[self.old].killcmd:
			if run(['which', self[self.old].killcmd[0]], 'call', quiet=True) == 0:
				run(self[self.old].killcmd, 'call')
				time.sleep(1)

		if self.active and self.old and 'noreplace' in self[self.active].flags:
			run(['killall', self[self.old].base], 'call')
			time.sleep(1)

		if self.active == 'compiz':
			# use a copy, not the original
			compiz_command = self['compiz'].command[:]
			for option in options:
				if options[option].enabled:
					compiz_command.append(options[option].switch)	

			kill_list = ['killall']
			for decorator in decorators:
				kill_list.append(decorators[decorator].base)
			run(kill_list, 'call')
			
			time.sleep(0.5)

			# do it
			print ' ... executing:', ' '.join(compiz_command)
			run(compiz_command, quiet=False)

		elif self.active:
			run(self[self.active].command)

		else:
			print ' * No active WM set; not going to do anything.'

	def restart(self):
		if wms.active:
			print ' * Reloading %s' %wms.active
			self.start()

		else:
			print ' * Not reloading, no active window manager set'

	active = property(__get, __set)

class CompizDecorator(object):

	def __init__(self, name, decorators, installed):

		self.decorators = decorators
		self.name = name
		self.base = installed.decorators[name][0]
		self.command = installed.decorators[name][1]
		self.label = installed.decorators[name][2]
		self.desktop = installed.decorators[name][3]

	def kill_others(self):
		killall = ['killall']
		for decorator in [x for x in self.decorators if x != self.name]:
			killall.append(self.decorators[decorator].base)
		run(killall, 'call')

class CompizDecorators(dict):
		
	def __init__(self, installed):

		# Open CompizConfig context
		if parser_options.verbose:
			print ' * Opening CompizConfig context'

		try:
			context = compizconfig.Context( \
				plugins=['decoration'], basic_metadata=True)

		except:
			context = compizconfig.Context()

		self.command = context.Plugins['decoration'].Display['command']

		for decorator in installed.decorators:
			self[decorator] = CompizDecorator(decorator, self, installed)

		self.default = None
		decorator = [d for d in self if self[d].desktop == env.desktop]
		if decorator:
			self.default = decorator[0]

		elif 'emerald' in self:
			self.default = 'emerald'

		elif self:                       
			self.default = self.keys()[0]
	
	def __set(self, decorator):
		if decorator in self:
			self.command.Plugin.Context.ProcessEvents()
			print ' * Setting decorator to %s ("%s")' \
				%(self[decorator].label, self[decorator].command)
			self.command.Value = self[decorator].command
			self.command.Plugin.Context.Write()
		elif not decorator:
			print ' * Not setting decorator to none'

	def __get(self):
		_decorator = [d for d in self if self.command.Value == self[d].command]
		if _decorator:
			decorator = _decorator[0]
		else:
			print ' * Decorator "%s" is invalid.' %self.command.Value
			self.active = self.default
			decorator = self.command.Value
		return decorator

	active = property(__get, __set)

class Installed(object):

	def __init__(self, data):
		print ' * Searching for installed applications...'

		### Compiz Detection
		bins = {}
		for name in ('compiz', 'compiz.real'):
			bin = run(['which', name], 'output')
			if bin:
				bins[name] = bin

		if 'compiz' in bins and 'compiz.real' in bins:
			if bins['compiz'].split(os.sep)[:-1] == bins['compiz.real'].split(os.sep)[:-1]:
				compiz = 'compiz.real'
			else:
				compiz = 'compiz'

		elif 'compiz.real' in bins:
			compiz = 'compiz.real'

		elif 'compiz' in bins:
			compiz = 'compiz'

		else:
			compiz = None

		output = ''

		for name in bins:
			if len(bins) > 1 and name == compiz:
				selected = ' <*>'
			else:
				selected = ''
			output += ' -- %s%s' %(bins[name], selected)

		### Everything Else
		self.wms = data.wms.copy()
		for wm in data.wms:
			which = run(['which', data.wms[wm][0]], 'output')
			if which:
				output += ' -- %s' %which
			else:
				del self.wms[wm]

		if compiz:
			data.compiz_args.insert(0, compiz)
			self.wms['compiz'] = (compiz, data.compiz_args, 'Compiz', None, None, None)

		self.decorators = data.decorators.copy()
		for decorator in data.decorators:
			which = run(['which', data.decorators[decorator][0]], 'output')
			if which:
				output += ' -- %s' %which
			else:
				del self.decorators[decorator]

		self.apps = data.apps.copy()
		for app in data.apps:
			which = run(['which', data.apps[app][0]], 'output')
			if which:
				output += ' -- %s' %which
			else:
				del self.apps[app]

		if parser_options.verbose:
			print output.rstrip()
		
		compiz_optionlist = []

		self.options = data.options.copy()

		if compiz:
			compiz_help = run([compiz, '--help'], 'output')
			for item in compiz_help.split():
				item = item[1:].replace(']', '')
				if item.startswith('--'):
					compiz_optionlist.append(item)

		for option in data.options:
			if data.options[option][1] not in compiz_optionlist:
				del self.options[option]

class Configuration(ConfigParser.ConfigParser):

	def __init__(self, data):
		
		ConfigParser.ConfigParser.__init__(self)
		self.config_folder = data.config_folder
		self.config_file = data.config_file

	def check(self):

		# Configuration file setup
		if not os.path.exists(self.config_folder):
			if parser_options.verbose: 
				print ' * Creating configuration folder...'
			os.makedirs(self.config_folder)

		if not os.path.exists(self.config_file):
			if parser_options.verbose:
				print ' * Creating configuration file...'
			self.create_config_file()

		try:
			# Read the file
			self.read(self.config_file)
			# Validate the file by trying to read all values
			for option in options:
				value = options[option].enabled
			value = wms.active

		except:
			# back it up and make a new one
			print ' * Configuration file (%s) invalid' %self.config_file
			self.reset_config_file()
			print ' * Generating new configuration file'
			self.create_config_file()

	def create_config_file(self):
		'Set default values for configuration file'

		def prune(section, optlist):
			for option in [o for o in self.options(section) if o not in optlist]:
				self.remove_option(section, option)

		for section in ('compiz options', 'window manager'):
			if not self.has_section(section):
				self.add_section(section)

		for option in options:
			self.set('compiz options', option, 'false')
		self.set('window manager', 'active wm', 'compiz')

		prune('compiz options', options)
		prune('window manager', ['active wm'])
		self.write(open(self.config_file, 'w'))

	def reset_config_file(self):
		'Backup configuration file'

		if os.path.exists(self.config_file):
			config_backup = '%s.backup.%s' \
				%(self.config_file, time.strftime('%Y%m%d%H%M%S'))
			os.rename(self.config_file, config_backup)
			print ' ... backed up to:', config_backup
		else:
			print ' ... no configuration file found'

# Instantiate...
_installed = Installed(_data)
config = Configuration(_data)
apps = Applications(_installed)
options = CompizOptions(_installed, config)
wms = WindowManagers(_installed, config)
decorators = CompizDecorators(_installed)

