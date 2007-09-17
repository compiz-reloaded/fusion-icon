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

# Author(s): xsacha

import sys, os, time
from PyQt4 import QtGui, QtCore
from FusionIcon.start import wms, apps, options, decorators, init

class Build(QtGui.QApplication):
	def reload_wm(self):
		wms.restart()
	def toggleWM(self, wm):
		if wms.active != wm:
			wms.active = wm
			wms.start()
	def toggleOP(self, option):
		options[option].enabled = not options[option].enabled
		if wms.active == 'compiz':
			wms.start()
	def toggleWD(self, decorator):
		decorators[decorator].kill_others()
		time.sleep(0.5)
		decorators.active = decorator
	def __init__(self, parent=None):
		QtCore.QObject.__init__(self, parent)
		# Qt sucks (I'm aware this breaks if prefix != /usr...)
		self.Tray = QtGui.QSystemTrayIcon(QtGui.QIcon('/usr/share/icons/hicolor/22x22/apps/fusion-icon.png'))
		self.Tray.setToolTip('Compiz Fusion Icon')
		self.Tray.managerMenu = QtGui.QMenu()
		self.Tray.optionsMenu = QtGui.QMenu()
		self.Tray.decoratorMenu = QtGui.QMenu()
		self.groupManager = QtGui.QActionGroup(self.Tray.managerMenu)
		self.groupDecorator = QtGui.QActionGroup(self.Tray.decoratorMenu)
		for wm in wms.ordered_list:
			actionWM = self.groupManager.addAction(self.Tray.managerMenu.addAction(wms[wm].label, lambda val=wm : self.toggleWM(val)))
			actionWM.setCheckable(True)
			if wms.active == wm:
				actionWM.setChecked(True)
		for option in options:
			actionOP = self.Tray.optionsMenu.addAction(options[option].label, lambda val=option: self.toggleOP(val))
			actionOP.setCheckable(True)
			if not options[option].sensitive:
				actionOP.setEnabled(False)
			actionOP.setChecked(options[option].enabled)
		for decorator in decorators:
			actionWD = self.groupDecorator.addAction(self.Tray.decoratorMenu.addAction(decorators[decorator].label, lambda val=decorator: self.toggleWD(val)))
			actionWD.setCheckable(True)
			if decorators.active == decorator:
				actionWD.setChecked(True)
		self.Tray.menu = QtGui.QMenu()
		if 'ccsm' in apps:
			self.Tray.menu.addAction(apps['ccsm'].label, lambda: run(['ccsm']))
		if 'emerald theme manager' in apps:
			self.Tray.menu.addAction(apps['emerald theme manager'].label, lambda: run(apps['emerald theme manager'].command))
		if 'ccsm' in apps or 'emerald theme manager' in apps:
			self.Tray.menu.addSeparator()
		self.Tray.menu.addAction("Reload Window Manager", self.reload_wm)
		self.Tray.menu.addAction("Select Window Manager").setMenu(self.Tray.managerMenu)
		self.Tray.menu.addAction("Compiz Options").setMenu(self.Tray.optionsMenu)
		self.Tray.menu.addAction("Select Window Decorator").setMenu(self.Tray.decoratorMenu)
		self.Tray.menu.addSeparator()
		self.Tray.menu.addAction("Quit", self.quit)
		self.Tray.setContextMenu(self.Tray.menu)
		self.Tray.show()
		init()
Build(sys.argv).exec_()

