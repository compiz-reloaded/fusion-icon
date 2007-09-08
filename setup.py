#!/usr/bin/env python

import sys, os
from stat import *
from distutils.core import setup
from distutils.command.install import install as _install

INSTALLED_FILES = '.installed_files'

#stolen from ccsm
class install (_install):

	def run (self):

		_install.run(self)
		outputs = self.get_outputs()
		data = '\n'.join(outputs)
		try:
			f = open(INSTALLED_FILES, 'w')
		except:
			self.warn ('Could not write installed files list %s' %INSTALLED_FILES)
			return 

		f.write(data)
		f.close()

class uninstall(_install):

	def run(self):
		try:
			files = file(INSTALLED_FILES, 'r').readlines()
		except:
			self.warn('Could not read installed files list %s' %INSTALLED_FILES)
			return

		for f in files:
			print 'Uninstalling %s' %f.strip()
			try:
				os.unlink(f.strip())
			except:
				self.warn('Could not remove file %s' %f)
		os.remove(INSTALLED_FILES)

version = open('VERSION', 'r').read().strip()	

packages = ['FusionIcon']

available_interfaces = {
	'gtk': 'FusionIcon.interface_gtk',
	'qt4': 'FusionIcon.interface_qt4',
#	'qt3': 'FusionIcon.interface_qt3',
}

#if 'interfaces' in os.environ:
# 	for interface in os.environ['interfaces'].split():
#		if interface in available_interfaces:
#			packages.append(available_interfaces[interface])
#else:

packages.extend(available_interfaces.values())


data_files = [
	('share/icons/hicolor/22x22/apps',['images/22x22/fusion-icon.png']),
	('share/icons/hicolor/24x24/apps',['images/24x24/fusion-icon.png']),
	('share/icons/hicolor/48x48/apps',['images/48x48/fusion-icon.png']),
	('share/icons/hicolor/scalable/apps',['images/scalable/fusion-icon.svg']),
	('share/applications',['fusion-icon.desktop']),
]


setup(
	name='fusion-icon',
	version=version,
	description='User-friendly tray icon for launching and managing Compiz Fusion',
	author='Christopher Williams',
	author_email='christopherw@verizon.net',
	url='http://opencompositing.org',
	packages=packages,
	scripts=['fusion-icon'],
	data_files=data_files,
	cmdclass={
		'uninstall': uninstall,
		'install': install},
)

#Stolen from ccsm's setup.py
if sys.argv[1] == 'install':
	
	prefix = None

	if len (sys.argv) > 2:
		i = 0
		for o in sys.argv:
			if o.startswith ("--prefix"):
				if o == "--prefix":
					if len (sys.argv) >= i:
						prefix = sys.argv[i + 1]
					sys.argv.remove (prefix)
				elif o.startswith ("--prefix=") and len (o[9:]):
					prefix = o[9:]
				sys.argv.remove (o)
				break
			i += 1

	if not prefix:
		prefix = '/usr'

	gtk_update_icon_cache = '''gtk-update-icon-cache -f -t \
%s/share/icons/hicolor''' % prefix
	root_specified = [s for s in sys.argv if s.startswith('--root')]
	if not root_specified or root_specified[0] == '--root=/':
		print 'Updating Gtk icon cache.'
		os.system(gtk_update_icon_cache)
	else:
		print '''*** Icon cache not updated. After install, run this:
***     %s''' % gtk_update_icon_cache

