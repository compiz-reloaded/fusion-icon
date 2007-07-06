#!/usr/bin/env python
# Author(s): xsacha
import sys
from time import sleep
from PyQt4 import QtGui, QtCore
from libfusionicon import *

#Defs
def lockItem(action,b):
    if b:
        action.setChecked(True)
        action.setEnabled(False)
    else:
        action.setChecked(False)
        action.setEnabled(True)
def open_ccsm():
    Popen(['ccsm'])
def open_emeraldthemes():
    Popen(['emerald-theme-manager'])
def reload_wm():
    print '* Reloading Window Manager ...'
    start_wm()
def run_wm(str):
    if active_wm != str:
        set_setting('window manager', 'active wm', str)
        configuration.write(open(config_file, 'w'))
        print '* switching to', str,'...'
        start_wm()
def runCompiz():
    run_wm(compiz)
def runMetacity():
    run_wm('metacity')
def runKwin():
    run_wm('kwin')
def runXfwm4():
    run_wm('xfwm4')
def toggleIR():
    if int(get_setting('compiz options', 'indirect rendering')):
        print '* disabling Indirect Rendering...'
        set_setting('compiz options', 'indirect rendering', '0')
    else:
        print '* enabling  Indirect Rendering...'
        set_setting('compiz options', 'indirect rendering', '1')
    configuration.write(open(config_file, 'w'))
    if active_wm == compiz:
        reload_wm()
def toggleLB():
    if int(get_setting('compiz options', 'loose binding')):
        print '* disabling Loose Binding...'
        set_setting('compiz options', 'loose binding', '0')
    else:
        print '* enabling  Loose Binding...'
        set_setting('compiz options', 'loose binding', '1')
    configuration.write(open(config_file, 'w'))
    if active_wm == compiz:
        reload_wm()
def toggleEmerald():
    system('killall kde-window-decorator gtk-window-decorator 2>/dev/null')
    lockItem(actionGWD, False)
    lockItem(actionKWD, False)
    lockItem(actionEmerald, True)
    set_decorator(emerald)
def toggleGWD():
    system('killall kde-window-decorator emerald 2>/dev/null')
    lockItem(actionEmerald, False)
    lockItem(actionKWD, False)
    lockItem(actionGWD, True)	
    set_decorator(gwd)
def toggleKWD():
    system('killall emerald gtk-window-decorator 2>/dev/null')
    set_decorator(kwd)
    lockItem(actionEmerald, False)
    lockItem(actionGWD, False)
    lockItem(actionKWD, True)

#Run Menu
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
app = QtGui.QApplication(sys.argv)

SysTray = QtGui.QSystemTrayIcon(QtGui.QIcon('/usr/share/pixmaps/fusion-icon.png'))
SysTray.setToolTip("Compiz Fusion Icon")

SysTray.managerMenu = QtGui.QMenu()
if compiz != '':
    SysTray.managerMenu.addAction("Compiz",runCompiz)
if is_installed('metacity'):
    SysTray.managerMenu.addAction("Metacity",runMetacity)
if is_installed('kwin'):
    SysTray.managerMenu.addAction("Kwin",runKwin)
if is_installed('xfwm4'):
    SysTray.managerMenu.addAction("Xfwm4",runXfwm4)

SysTray.optionsMenu = QtGui.QMenu()
actionIR = SysTray.optionsMenu.addAction("Indirect Rendering",toggleIR)
actionIR.setCheckable(True)
actionLB = SysTray.optionsMenu.addAction("Loose Binding",toggleLB)
actionLB.setCheckable(True)
if always_indirect:
    lockItem(actionIR, True)
elif indirect_rendering:
    actionIR.setChecked(True)
if loose_binding:
    actionLB.setChecked(True)

SysTray.decoratorMenu = QtGui.QMenu()
actionEmerald = SysTray.decoratorMenu.addAction("Emerald",toggleEmerald)
actionEmerald.setCheckable(True)
if is_installed('emerald'):
    if decosetting.Value == emerald:
        lockItem(actionEmerald, True)
else:
    actionEmerald.setVisible(False)
actionGWD = SysTray.decoratorMenu.addAction("GTK Decorator",toggleGWD)
actionGWD.setCheckable(True)
if is_installed('gtk-window-decorator'):
    if decosetting.Value == gwd:
         lockItem(actionGWD, True)
else:
    actionGWD.setVisible(False)
actionKWD = SysTray.decoratorMenu.addAction("KDE Decorator",toggleKWD)
actionKWD.setCheckable(True)
if is_installed('kde-window-decorator'):
    if decosetting.Value == kwd:
         lockItem(actionKWD, True)
else:
    actionKWD.setVisible(False)

SysTray.menu = QtGui.QMenu()
SysTray.menu.addAction("Settings Manager",open_ccsm)
SysTray.menu.addAction("Emerald Theme Manager",open_emeraldthemes)
SysTray.menu.addSeparator()
SysTray.menu.addAction("Reload Window Manager",reload_wm)
SysTray.menu.addAction("Select Window Manager").setMenu(SysTray.managerMenu)
SysTray.menu.addAction("Compiz Options").setMenu(SysTray.optionsMenu)
SysTray.menu.addAction("Select Window Decorator").setMenu(SysTray.decoratorMenu)
SysTray.menu.addSeparator()
SysTray.menu.addAction("Quit",app.quit)
SysTray.setContextMenu(SysTray.menu)
SysTray.show()
app.exec_()

