#!/usr/bin/env python
# Author(s): xsacha
import sys
from qt import *
import ctypes as c
from libfusionicon import *

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
        trayWin  = self.winId();

        iscreen = XScreenNumberOfScreen(XDefaultScreenOfDisplay(dpy))
        # get systray window (holds _NET_SYSTEM_TRAY_S<screen> atom)
        selectionAtom = XInternAtom(dpy, "_NET_SYSTEM_TRAY_S%i" % iscreen, 0)
        XGrabServer(dpy)
        managerWin = XGetSelectionOwner(dpy, selectionAtom)
        if managerWin != 0:
            # set StructureNotifyMask (1L << 17)
            XSelectInput(dpy, managerWin, 1L << 17)
        XUngrabServer(dpy);
        XFlush(dpy);
        if managerWin != 0:
            # send "SYSTEM_TRAY_OPCODE_REQUEST_DOCK to managerWin
            k = data()
            k.l = (0, # CurrentTime
                   0, # REQUEST_DOCK
                   trayWin, # window ID
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
        self.setPixmap(QPixmap('/usr/share/pixmaps/fusion-icon.png'))
        self.setAlignment(Qt.AlignHCenter)
        QToolTip.add(self, "Compiz Fusion Icon")

    def mousePressEvent(self, e):
        
        self.actionCompizWM=QAction("Compiz",0,self)
        self.actionCompizWM.setToggleAction(True)
        if active_wm == compiz:
            self.actionCompizWM.toggle()
        def compiz_slot():
            set_setting('window manager', 'active wm', compiz)
            start_wm()
        self.connect(self.actionCompizWM,SIGNAL("activated()"),compiz_slot)
        self.actionMetacityWM=QAction("Metacity",0,self)
        self.actionMetacityWM.setToggleAction(True)
        if active_wm == 'metacity':
            self.actionMetacityWM.toggle()
        def metacity_slot():
            set_setting('window manager', 'active wm', 'metacity')
            start_wm()
        self.connect(self.actionMetacityWM,SIGNAL("activated()"),metacity_slot)
        self.actionKwinWM=QAction("Kwin",0,self)
        self.actionKwinWM.setToggleAction(True)
        if active_wm == 'kwin':
            self.actionKwinWM.toggle()
        def kwin_slot():
            set_setting('window manager', 'active wm', 'kwin')
            start_wm()
        self.connect(self.actionKwinWM,SIGNAL("activated()"),kwin_slot)
        self.actionXfwm4WM=QAction("Xfwm4",0,self)
        self.actionXfwm4WM.setToggleAction(True)
        if active_wm == 'xfwm4':
            self.actionXfwm4WM.toggle()
        def xfwm4_slot():
            set_setting('window manager', 'active wm', 'xfwm4')
            start_wm()
        self.connect(self.actionXfwm4WM,SIGNAL("activated()"),xfwm4_slot)

        self.actionIndirectRender=QAction("Indirect Rendering",0,self)
        self.actionIndirectRender.setToggleAction(True)
        if indirect_rendering != '':
            self.actionIndirectRender.toggle()
        def indirectrender_slot():
            if indirect_rendering:
                set_setting('compiz options', 'indirect rendering', 1)
            else:
                set_setting('compiz options', 'indirect rendering', 0)
            if active_wm == compiz and initialized:
                start_compiz()
        self.connect(self.actionIndirectRender,SIGNAL("activated()"),indirectrender_slot)
        self.actionLooseBinding=QAction("Loose Binding",0,self)
        self.actionLooseBinding.setToggleAction(True)
        if loose_binding:
            self.actionLooseBinding.toggle()
        def loosebinding_slot():
            if loose_binding:
                set_setting('compiz options', 'loose binding', 1)
            else:
                set_setting('compiz options', 'loose binding', 0)
            if active_wm == compiz and initialized:
                start_compiz()
        self.connect(self.actionLooseBinding,SIGNAL("activated()"),loosebinding_slot)

        self.actionEmeraldWD=QAction("Emerald",0,self)
        def emerald_slot():
            if initialized:
                if active_wm == compiz and get_decorator() != emerald:
                        #remove the '--replace' (and any other arguments)
                        old_dec_list = get_decorator().split()
                        old_decorator = old_dec_list[0]
                        system('killall %s' % (old_decorator))
                        sleep(1)
                set_decorator(emerald)
        self.connect(self.actionEmeraldWD,SIGNAL("activated()"),emerald_slot)
        self.actionGTKWD=QAction("GTK Window Decorator",0,self)
        def GTK_slot():
            if initialized:
                if active_wm == compiz and get_decorator() != gwd:
                        old_dec_list = get_decorator().split()
                        old_decorator = old_dec_list[0]
                        system('killall %s' % (old_decorator))
                        sleep(1)
                set_decorator(gwd)
        self.connect(self.actionGTKWD,SIGNAL("activated()"),GTK_slot)
        self.actionKDEWD=QAction("KDE Window Decorator",0,self)
        def KDE_slot():
            if initialized:
                if active_wm == compiz and get_decorator() != kwd:
                        old_dec_list = get_decorator().split()
                        old_decorator = old_dec_list[0]
                        system('killall %s' % (old_decorator))
                        sleep(1)
                set_decorator(kwd)
        self.connect(self.actionKDEWD,SIGNAL("activated()"),KDE_slot)

        self.managerMenu = QPopupMenu()
        self.optionsMenu = QPopupMenu()
        self.decoratorMenu = QPopupMenu()

        if compiz != '':
            self.actionCompizWM.addTo(self.managerMenu)
        if installed('metacity'):
            self.actionMetacityWM.addTo(self.managerMenu)
        if installed('kwin'):
            self.actionKwinWM.addTo(self.managerMenu)
        if installed('xfwm4'):
            self.actionXfwm4WM.addTo(self.managerMenu)

        self.actionIndirectRender.addTo(self.optionsMenu)
        if always_indirect:
            self.actionIndirectRender.setEnabled(False)
        self.actionLooseBinding.addTo(self.optionsMenu)

        self.actionEmeraldWD.addTo(self.decoratorMenu)
        if not installed('emerald'):
            self.actionEmeraldWD.setEnabled(False)
        self.actionGTKWD.addTo(self.decoratorMenu)
        if not installed('gtk-window-decorator'):
            self.actionGTKWD.setEnabled(False)
        self.actionKDEWD.addTo(self.decoratorMenu)
        if not installed('kde-window-decorator'):
            self.actionKDEWD.setEnabled(False)

        contextMenu = QPopupMenu()
        menuSettings = contextMenu.insertItem("Settings Manager")
        menuEmerald = contextMenu.insertItem("Emerald Theme Manager")
        contextMenu.insertSeparator()
        menuReload = contextMenu.insertItem("Reload Window Manager")
        menuManager = contextMenu.insertItem("Select Window Manager",self.managerMenu)
        menuOptions = contextMenu.insertItem("Compiz Options",self.optionsMenu)
        menuDecorator = contextMenu.insertItem("Select Window Decorator",self.decoratorMenu)
        contextMenu.insertSeparator()
        menuQuit = contextMenu.insertItem("Quit")

        if e.button() == Qt.RightButton:
            id = contextMenu.exec_loop(e.globalPos())
            if id == menuSettings:
                Popen(['ccsm'])
            elif id == menuEmerald:
                etm_menu_activate(None)
            elif id == menuReload:
                wm_activate(None)
            elif id == menuQuit:
                self.emit(PYSIGNAL("endIcon()"), ())

app = QApplication(sys.argv)
SysTray = SystrayIcon("Fusion")
SysTray.show()
initialized = True
start_wm()
QObject.connect(SysTray,PYSIGNAL("endIcon()"), app.quit) 
app.exec_loop()
