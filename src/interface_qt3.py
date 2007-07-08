#!/usr/bin/env python
# Author(s): xsacha
import sys
from qt import *
import ctypes as c
from libfusionicon import *

app = QApplication(sys.argv)

# Defs
def run_wm(str):
    if get_setting('window manager', 'active wm') != str:
        set_setting('window manager', 'active wm', str)
        print '* switching to', str+'...'
        start_wm()
def run_wm_slot(act):
    if act == actionCompizWM:
        run_wm('compiz')
    elif act == actionMetacityWM:
        run_wm('metacity')
    elif act == actionKwinWM:
        run_wm('kwin')
    elif act == actionXfwm4WM:
        run_wm('xfwm4')
def ir_slot(on):
    set_setting('compiz options', 'indirect rendering', on)
    print '* indirect rendering is now %s' % bool(on)
    if get_setting('window manager', 'active wm') == compiz:
        start_compiz()
def lb_slot(on):
    set_setting('compiz options', 'loose binding', on)
    print '* loose binding is now %s' % bool(on)
    if get_setting('window manager', 'active wm') == compiz:
        start_compiz()
def run_wd_slot(act):
    os.system('killall emerald kde-window-decorator gtk-window-decorator 2>/dev/null')
    if act == actionEmeraldWD:
        set_decorator(emerald)
    elif act == actionGTKWD:
        set_decorator(gwd)
    elif act == actionKDEWD:
        set_decorator(kwd)

# Class
class SystrayIcon(QLabel):
    def __init__(self, icon, parent = None, name = "Fusion-Icon"):
        QLabel.__init__(self, parent, name, Qt.WMouseNoMask |\
           Qt.WRepaintNoErase | Qt.WType_TopLevel | Qt.WStyle_Customize |\
           Qt.WStyle_NoBorder | Qt.WStyle_StaysOnTop)
        self.setMinimumSize(22,22);
        self.setBackgroundMode(Qt.X11ParentRelative)
        self.setBackgroundOrigin(QWidget.WindowOrigin)

        libX11 = c.cdll.LoadLibrary("/usr/lib/libX11.so")
        # get all functions, set arguments + return types
        XDefaultScreenOfDisplay = libX11.XDefaultScreenOfDisplay
        XDefaultScreenOfDisplay.argtypes = [c.c_void_p]
        XDefaultScreenOfDisplay.restype = c.c_void_p

        XScreenNumberOfScreen = libX11.XScreenNumberOfScreen
        XScreenNumberOfScreen.argtypes = [c.c_void_p]

        XInternAtom = libX11.XInternAtom
        XInternAtom.argtypes = [c.c_void_p, c.c_char_p, c.c_int]

        XGrabServer = libX11.XGrabServer
        XGrabServer.argtypes = [c.c_void_p]

        XGetSelectionOwner = libX11.XGetSelectionOwner
        XGetSelectionOwner.argtypes = [c.c_void_p, c.c_int]

        XSelectInput = libX11.XSelectInput
        XSelectInput.argtypes = [c.c_void_p, c.c_int, c.c_long]

        XUngrabServer = libX11.XUngrabServer
        XUngrabServer.argtypes = [c.c_void_p]
        
        XFlush = libX11.XFlush
        XFlush.argtypes = [c.c_void_p]
        
        class data(c.Union):
            _fields_ = [("b", c.c_char * 20),
                        ("s", c.c_short * 10),
                        ("l", c.c_long * 5)]
        class XClientMessageEvent(c.Structure):
            _fields_ = [("type", c.c_int),
                        ("serial", c.c_ulong),
                        ("send_event", c.c_int),
                        ("display", c.c_void_p),
                        ("window", c.c_int),
                        ("message_type", c.c_int),
                        ("format", c.c_int),
                        ("data", data)]

        XSendEvent = libX11.XSendEvent
        XSendEvent.argtypes = [c.c_void_p, c.c_int, c.c_int, c.c_long, c.c_void_p]
                               
        XSync = libX11.XSync
        XSync.argtypes = [c.c_void_p, c.c_int]

        dpy = int(qt_xdisplay())

        iscreen = XScreenNumberOfScreen(XDefaultScreenOfDisplay(dpy))
        # get systray window (holds _NET_SYSTEM_TRAY_S<screen> atom)
        selectionAtom = XInternAtom(dpy, "_NET_SYSTEM_TRAY_S%i" % iscreen, 0)
        XGrabServer(dpy)
        managerWin = XGetSelectionOwner(dpy, selectionAtom)
        if managerWin != 0:
            # set StructureNotifyMask (1L << 17)
            XSelectInput(dpy, managerWin, 1L << 17)
        XUngrabServer(dpy)
        XFlush(dpy)
        if managerWin != 0:
            # send "SYSTEM_TRAY_OPCODE_REQUEST_DOCK to managerWin
            k = data()
            k.l = (0, # CurrentTime
                   0, # REQUEST_DOCK
                   self.winId(), # window ID
                   0, # empty
                   0) # empty
            ev = XClientMessageEvent(33, #type: ClientMessage
                                     0, # serial
                                     0, # send_event
                                     dpy, # display
                                     managerWin, # systray manager
                                     XInternAtom(dpy, "_NET_SYSTEM_TRAY_OPCODE", 0), 32, k)
            XSendEvent(dpy, managerWin, 0, 0, c.addressof(ev))
            XSync(dpy, 0)
        self.setPixmap(QPixmap('../icons/hicolor/22x22/apps/fusion-icon.png'))
        self.setAlignment(Qt.AlignHCenter)
        QToolTip.add(self, "Compiz Fusion Icon")

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            id = contextMenu.exec_loop(e.globalPos())
            if id == menuSettings:
                subprocess.Popen(['ccsm'])
            elif id == menuEmerald:
                subprocess.Popen(['emerald-theme-manager'])
            elif id == menuReload:
                print '* reloading window manager...'
                start_wm()

#Menus
managerMenu = QPopupMenu()
optionsMenu = QPopupMenu()
decoratorMenu = QPopupMenu()

#Manager Menu
groupWM = QActionGroup(managerMenu, "groupWM", True)
actionCompizWM=QAction("Compiz", 0, groupWM)
actionCompizWM.setToggleAction(True)
actionMetacityWM=QAction("Metacity", 0, groupWM)
actionMetacityWM.setToggleAction(True)
actionKwinWM=QAction("Kwin", 0, groupWM)
actionKwinWM.setToggleAction(True)
actionXfwm4WM=QAction("Xfwm4", 0, groupWM)
actionXfwm4WM.setToggleAction(True)
active_wm = get_setting('window manager', 'active wm')
if active_wm == compiz:
    actionCompizWM.toggle()
if active_wm == 'metacity':
    actionMetacityWM.toggle()
if active_wm == 'kwin':
    actionKwinWM.toggle()
if active_wm == 'xfwm4':
    actionXfwm4WM.toggle()
QObject.connect(groupWM, SIGNAL("selected(QAction*)"), run_wm_slot)
if compiz == '':
    actionCompizWM.setEnabled(False)
if not is_installed('metacity'):
    actionMetacityWM.setEnabled(False)
if not is_installed('kwin'):
    actionKwinWM.setEnabled(False)
if not is_installed('xfwm4'):
    actionXfwm4WM.setEnabled(False)
groupWM.addTo(managerMenu)

#Options Menu
groupOptions = QActionGroup(optionsMenu, "groupOptions", False)
actionIndirectRender=QAction("Indirect Rendering", 0, groupOptions)
actionIndirectRender.setToggleAction(True)
actionLooseBinding=QAction("Loose Binding", 0, groupOptions)
actionLooseBinding.setToggleAction(True)
if int(get_setting('compiz options', 'indirect rendering')):
    actionIndirectRender.toggle()
if always_indirect:
    actionIndirectRender.setEnabled(False)
if int(get_setting('compiz options', 'loose binding')):
    actionLooseBinding.toggle()
QObject.connect(actionIndirectRender, SIGNAL("toggled(bool)"), ir_slot)
QObject.connect(actionLooseBinding, SIGNAL("toggled(bool)"), lb_slot)
groupOptions.addTo(optionsMenu)


#Decorator Menu
groupWD =  QActionGroup(decoratorMenu, "groupWD", True)
actionEmeraldWD=QAction("Emerald", 0, groupWD)
actionEmeraldWD.setToggleAction(True)
actionGTKWD=QAction("GTK Window Decorator", 0, groupWD)
actionGTKWD.setToggleAction(True)
actionKDEWD=QAction("KDE Window Decorator", 0, groupWD)
actionKDEWD.setToggleAction(True)
if decosetting.Value == emerald:
     actionEmeraldWD.toggle()
elif decosetting.Value == gwd:
    actionGTKWD.toggle()
elif decosetting.Value == kwd:
    actionKDEWD.toggle()
QObject.connect(groupWD, SIGNAL("selected(QAction*)"), run_wd_slot)
if not is_installed('emerald'):
    actionEmeraldWD.setEnabled(False)
if not is_installed('gtk-window-decorator'):
    actionGTKWD.setEnabled(False)
if not is_installed('kde-window-decorator'):
    actionKDEWD.setEnabled(False)
groupWD.addTo(decoratorMenu)

# Main Menu
contextMenu = QPopupMenu()
menuSettings = contextMenu.insertItem("Settings Manager")
menuEmerald = contextMenu.insertItem("Emerald Theme Manager")
contextMenu.insertSeparator()
menuReload = contextMenu.insertItem("Reload Window Manager")
menuManager = contextMenu.insertItem("Select Window Manager", managerMenu)
menuOptions = contextMenu.insertItem("Compiz Options", optionsMenu)
menuDecorator = contextMenu.insertItem("Select Window Decorator", decoratorMenu)
contextMenu.insertSeparator()
menuQuit = contextMenu.insertItem("Quit", app.quit)

#Run
SysTray = SystrayIcon("Fusion")
SysTray.show()
app.exec_loop()
