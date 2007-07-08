#!/usr/bin/env python
# Author(s): xsacha
import sys
from time import sleep
from PyQt4 import QtGui, QtCore
from libfusionicon import *

#Defs
def open_ccsm():
    subprocess.Popen(['ccsm'])
def open_emeraldthemes():
    subprocess.Popen(['emerald-theme-manager'])
def reload_wm():
    print '* Reloading Window Manager ...'
    start_wm()
def run_wm(str):
    if get_setting('window manager', 'active wm') != str:
        set_old_wm()
        set_setting('window manager', 'active wm', str)
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
    if get_setting('window manager', 'active wm') == compiz:
        reload_wm()
def toggleLB():
    if int(get_setting('compiz options', 'loose binding')):
        print '* disabling Loose Binding...'
        set_setting('compiz options', 'loose binding', '0')
    else:
        print '* enabling  Loose Binding...'
        set_setting('compiz options', 'loose binding', '1')
    if get_setting('window manager', 'active wm') == compiz:
        reload_wm()
def toggleEmerald():
    os.system('killall kde-window-decorator gtk-window-decorator 2>/dev/null')
    set_decorator(emerald)
def toggleGWD():
    os.system('killall kde-window-decorator emerald 2>/dev/null')
    set_decorator(gwd)
def toggleKWD():
    os.system('killall emerald gtk-window-decorator 2>/dev/null')
    set_decorator(kwd)

#Run Menu
#QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
app = QtGui.QApplication(sys.argv)

SysTray = QtGui.QSystemTrayIcon(QtGui.QIcon(sys.path[0] + '/../icons/hicolor/22x22/apps/fusion-icon.png'))
SysTray.setToolTip("Compiz Fusion Icon")

active_wm = get_setting('window manager', 'active wm')
SysTray.managerMenu = QtGui.QMenu()
groupManager = QtGui.QActionGroup(SysTray.managerMenu)
if compiz != '':
    actionCompiz = groupManager.addAction(SysTray.managerMenu.addAction("Compiz",runCompiz))
    actionCompiz.setCheckable(True)
    if active_wm == compiz:
        actionCompiz.setChecked(True)
if is_installed('metacity'):
    actionMetacity = groupManager.addAction(SysTray.managerMenu.addAction("Metacity",runMetacity))
    actionMetacity.setCheckable(True)
    if active_wm == 'metacity':
        actionMetacity.setChecked(True)
if is_installed('kwin'):
    actionKwin = groupManager.addAction(SysTray.managerMenu.addAction("Kwin",runKwin))
    actionKwin.setCheckable(True)
    if active_wm == 'kwin':
        actionKwin.setChecked(True)
if is_installed('xfwm4'):
    actionXfwm4 = groupManager.addAction(SysTray.managerMenu.addAction("Xfwm4",runXfwm4))
    actionXfwm4.setCheckable(True)
    if active_wm == 'xfwm4':
        actionXfwm4.setChecked(True)

SysTray.optionsMenu = QtGui.QMenu()
actionIR = SysTray.optionsMenu.addAction("Indirect Rendering",toggleIR)
actionIR.setCheckable(True)
actionLB = SysTray.optionsMenu.addAction("Loose Binding",toggleLB)
actionLB.setCheckable(True)
if indirect_rendering:
    actionIR.setChecked(True)
if always_indirect:
    actionIR.setEnabled(False)
if loose_binding:
    actionLB.setChecked(True)

SysTray.decoratorMenu = QtGui.QMenu()
groupDecorator = QtGui.QActionGroup(SysTray.decoratorMenu)
if is_installed('emerald'):
    actionEmerald = groupDecorator.addAction(SysTray.decoratorMenu.addAction("Emerald",toggleEmerald))
    actionEmerald.setCheckable(True)
    if decosetting.Value == emerald:
        actionEmerald.setChecked(True)
if is_installed('gtk-window-decorator'):
    actionGWD = groupDecorator.addAction(SysTray.decoratorMenu.addAction("GTK Decorator",toggleGWD))
    actionGWD.setCheckable(True)
    if decosetting.Value == gwd:
         actionGWD.setChecked(True)
if is_installed('kde-window-decorator'):
    actionKWD = groupDecorator.addAction(SysTray.decoratorMenu.addAction("KDE Decorator",toggleKWD))
    actionKWD.setCheckable(True)
    if decosetting.Value == kwd:
         actionKWD.setChecked(True)

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
