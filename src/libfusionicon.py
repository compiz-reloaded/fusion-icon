#!/usr/bin/env python
# Author(s): crdlb
import ConfigParser, compizconfig
from commands import getoutput
from os import mkdir, system, popen, path, environ, rename
from subprocess import Popen
from time import sleep, time

# Defining functions
def installed(app):
	global app_is_installed
	return app in app_is_installed

def default_decorator():
	if installed('kde-window-decorator') and kde and not gnome:
		decorator = kwd
	elif installed('gtk-window-decorator') and gnome and not kde:
		decorator = gwd
	elif installed('emerald'):
		decorator = emerald
	elif installed('gtk-window-decorator'):
		decorator = gwd
	elif installed('kde-window-decorator'):
		decorator = kwd
	if decorator != None:
		print '... choosing', decorator, 'as default decorator'
	else:
		print '*** Warning: no decorator installed'
	return decorator

def create_config_file():
	default_config = open(config_file, 'w')
	default_config.write('[compiz options]\nindirect rendering = 0\nloose binding = 0\n\n[window manager]\nactive wm = %s\n' %(compiz))
	default_config.close()

def fallback_wm():
	if installed('kwin') and kde and not gnome: wm = 'kwin'
	elif installed('metacity') and gnome and not kde: wm = 'metacity'
	else: wm = ''
	set_setting('window manager', 'active wm', wm)
	return wm

def env_intel():
	if not getoutput('xvinfo 2>/dev/null|grep Intel') == '':
		print '* intel found, exporting: INTEL_BATCH=1'
		return 'INTEL_BATCH=1 '
	else: return ''
	
def is_always_indirect():
	if int(getoutput('glxinfo 2>/dev/null | grep GLX_EXT_texture_from_pixmap -c')) < 3:
		if int(getoutput('LIBGL_ALWAYS_INDIRECT=1 glxinfo 2>/dev/null | grep GLX_EXT_texture_from_pixmap -c')) == 3:
			return True
		
def env_indirect():
	if is_always_indirect():
		print '* No GLX_EXT_texture_from_pixmap present with direct rendering context'
		print '... present with indirect rendering, exporting: LIBGL_ALWAYS_INDIRECT=1'
		return 'LIBGL_ALWAYS_INDIRECT=1 '
	else: return ''
		
def env_fglrx():
	if path.exists('/usr/lib/fglrx/libGL.so.1.2.xlibmesa'):
		print '* fglrx found, exporting: LD_PRELOAD=/usr/lib/fglrx/libGL.so.1.2.xlibmesa'
		return 'LD_PRELOAD=/usr/lib/fglrx/libGL.so.1.2.xlibmesa '
	else: return ''
	
def env_nvidia():
	if not getoutput('xdpyinfo 2>/dev/null|grep NV-GLX') == '':
		print '* nvidia found, exporting: __GL_YIELD=nothing '
		return '__GL_YIELD=nothing '
	else: return ''
	
def get_env():
	return env_intel() + env_indirect() + env_fglrx() + env_nvidia()

def start_wm():
	active_wm = get_setting('window manager', 'active wm')
	print "start_wm", active_wm
	if active_wm == compiz:
		start_compiz()
	else:
		run_wm = active_wm + ' --replace'
		Popen(run_wm, shell=True)

def start_compiz():
	env_variables = get_env()
	arg_indirect_rendering = arg_loose_binding = ''
	indirect_rendering = int(get_setting('compiz options', 'indirect rendering'))
	if indirect_rendering:
		arg_indirect_rendering = '--indirect-rendering'
	loose_binding = int(get_setting('compiz options', 'loose binding'))
	if loose_binding:
		arg_loose_binding = '--loose-binding'
	system('killall gtk-window-decorator kde-window-decorator emerald 2>/dev/null')
	#sleep(2)
	run_compiz = env_variables + compiz + ' --replace --sm-disable --ignore-desktop-hints ccp ' + arg_indirect_rendering + ' ' + arg_loose_binding
	print "Executing:", run_compiz
	Popen(run_compiz, shell=True)

	
def set_decorator(decorator):
	context.Read()
	context.ProcessEvents()
	decosetting.Value = decorator
	print '* setting decorator to', decosetting.Value
	context.Write()
		
def get_decorator():
	if decosetting.Value == emerald or decosetting.Value == kwd or decosetting.Value == gwd:
		decorator = decosetting.Value
	else:
		print '* Decorator "'+ decosetting.Value +'" is invalid.'
		decorator = default_decorator()
	return decorator

def set_setting(section, option, value):
	configuration.set(section, option, str(value))
	configuration.write(open(config_file, 'w'))

def get_setting(section, option):
	return configuration.get(section, option)

always_indirect = is_always_indirect()

#Open CompizConfig context
context = compizconfig.Context()
context.Read()
decoplugin = context.Plugins['decoration']
decosetting = compizconfig.Setting(decoplugin, 'command', 0)

# Get installed applications
print "* Getting installed applications..."
app_is_installed = []
apps = ('compiz.real', 'compiz' , 'ccsm' , 'gtk-window-decorator', 'kde-window-decorator', 'emerald' , 'metacity' , 'kwin', 'xfwm4') 
for application in apps:
	if system('which ' + application + ' 2>/dev/null') == 0:
		app_is_installed.append(application)

if installed('compiz.real'): compiz = 'compiz.real'
elif installed('compiz'): compiz = 'compiz'
gwd = 'gtk-window-decorator --replace'
kwd = 'kde-window-decorator --replace'
emerald = 'emerald --replace'

# Check whether GNOME or KDE running
kde = gnome = False
if system('pgrep gnome-session 1>/dev/null') == 0: gnome = True
if system('pgrep dcop 1>/dev/null') == 0: kde = True

print '* gnome is', str(gnome) + '; kde is', str(kde)

active_decorator = get_decorator()
set_decorator(active_decorator)

# Variables
config_folder = environ.get('XDG_CONFIG_HOME', path.join(environ.get('HOME'), '.config'))  
config_file = path.join(config_folder, 'fusion-icon')

# Configuration file setup
if not path.exists(config_folder):
	mkdir(config_folder)
	create_config_file()
elif not path.exists(config_file):
	create_config_file()

# Retrieve configuration from ~/.config/fusion-icon
try:
	configuration = ConfigParser.ConfigParser()
	configuration.read(config_file)
	active_wm = get_setting('window manager', 'active wm')
	indirect_rendering = int(get_setting('compiz options', 'indirect rendering'))
	loose_binding = int(get_setting('compiz options', 'loose binding'))
except:
	print "* Configuration file (" + config_file + ") invalid"
	if path.exists(config_file):
		config_backup = path.join(config_folder, 'fusion-icon.backup.' + str(int(time())))
		rename(config_file, config_backup)
		print "... backed up to:", config_backup
	print "* Generating new configuration file"
	create_config_file()
	configuration = ConfigParser.ConfigParser()
	configuration.read(config_file)
	active_wm = get_setting('window manager', 'active wm')
	indirect_rendering = int(get_setting('compiz options', 'indirect rendering'))
	loose_binding = int(get_setting('compiz options', 'loose binding'))

if not installed(active_wm):
	print '* ' + active_wm + ' not installed'
	active_wm = fallback_wm()
	print '... setting to fallback: ' + active_wm
if always_indirect:
	set_setting('compiz options', 'indirect rendering', 1)

start_wm()
