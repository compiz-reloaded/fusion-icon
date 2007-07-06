#!/usr/bin/env python
# Author(s): crdlb, nesl247
import ConfigParser, compizconfig
from commands import getoutput
from os import mkdir, system, popen, path, environ, rename
from subprocess import Popen
from time import time

# Define variables
fglrx_locations=('/usr/lib/fglrx/libGL.so.1.2.xlibmesa', '/opt/mesa-xgl/lib/libGL.so.1.2')

apps = ('compiz.real', 'ccsm', 'compiz', 'gtk-window-decorator', 'kde-window-decorator', 'emerald', 'metacity', 'kwin', 'xfwm4') 
wmlist = ('compiz', 'xfwm4', 'kwin', 'metacity')

emerald = 'emerald --replace'
kwd = 'kde-window-deocrator --replace'
gwd = 'gtk-window-decorator --replace'
decorators = (gwd, kwd, emerald)


# Defining functions
def is_running(app):
	if system('pgrep ' + app + ' 1>/dev/null') == 0:
		return True
	else:
		return False

def is_installed(app):
	global app_is_installed
	return app in apps_installed

def default_decorator():
	'Find the default decorator to use'

	# Use kwd if kde but not gnome
	if is_installed('kde-window-decorator') and kde and not gnome:
		decorator = kwd

	# Use gwd if gnome but not kde
	elif is_installed('gtk-window-decorator') and gnome and not kde:
		decorator = gwd

	# Use emerald otherwise
	elif is_installed('emerald'):
		decorator = emerald
		
	# Use what is available
	elif is_installed('gtk-window-decorator'):
		decorator = gwd
	elif is_installed('kde-window-decorator'):
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
	'Return a fallback window manager'

	if is_installed('kwin') and kde and not gnome:
		wm = 'kwin'

	elif is_installed('metacity') and gnome and not kde:
		wm = 'metacity'
		
	elif is_installed('xfwm4') and not kde and not gnome and xfce4:
		wm = 'xfwm4'

	else:
		wm = ''

	set_setting('window manager', 'active wm', wm)
	return wm

def env_intel():
	'Determines if we are using intel'

	if not getoutput('xvinfo 2>/dev/null|grep Intel') == '':
		print '* Intel found, exporting: INTEL_BATCH=1'
		return 'INTEL_BATCH=1 '
	else:
		return ''
	
def is_always_indirect():
	'Determines if we are always using indirect rendering'

	if int(getoutput('glxinfo 2>/dev/null | grep GLX_EXT_texture_from_pixmap -c')) < 3:
		if int(getoutput('LIBGL_ALWAYS_INDIRECT=1 glxinfo 2>/dev/null | grep GLX_EXT_texture_from_pixmap -c')) == 3:
			return True
		
def env_indirect():
	'Determines if we are using indirect rendering'

	if is_always_indirect():
		print '* No GLX_EXT_texture_from_pixmap present with direct rendering context'
		print '... present with indirect rendering, exporting: LIBGL_ALWAYS_INDIRECT=1'
		return 'LIBGL_ALWAYS_INDIRECT=1 '
	else:
		return ''
		
def env_fglrx():
	'Determines if we are using fglrx'
	
	for x in fglrx_locations:
		if os.path.exists(location):
			print '* fglrx found, exporting: LD_PRELOAD=' + location + ' '
			return 'LD_PRELOAD=' + location + ' '
	# We've not found anything
	return ''
	
def env_nvidia():
	'Determines if we are using nvidia'

	if not getoutput('xdpyinfo 2>/dev/null|grep NV-GLX') == '':
		print '* nvidia found, exporting: __GL_YIELD="NOTHING" '
		return '__GL_YIELD="NOTHING" '
	else:
		return ''
	
def get_env():
	return env_intel() + env_indirect() + env_fglrx() + env_nvidia()

def start_wm():
	active_wm = get_setting('window manager', 'active wm')

	if active_wm == compiz:
		start_compiz()
	else:
		print "* Starting:", active_wm
		Popen(active_wm + ' --replace', shell=True)

def start_compiz():
	env_variables = get_env()

	arg_indirect_rendering = arg_loose_binding = ''
	indirect_rendering = int(get_setting('compiz options', 'indirect rendering'))

	if indirect_rendering:
		arg_indirect_rendering = ' --indirect-rendering '
	
	loose_binding = int(get_setting('compiz options', 'loose binding'))
	if loose_binding:
		arg_loose_binding = ' --loose-binding '

	run_compiz = env_variables + compiz + ' --replace --sm-disable --ignore-desktop-hints ccp' + arg_indirect_rendering + arg_loose_binding
	print '* Starting:', run_compiz
	Popen(run_compiz, shell=True)

	
def set_decorator(decorator):
	'Sets the decorator via libcompizconfig'

	context.Read()
	context.ProcessEvents()
	decosetting.Value = decorator
	print '* Setting decorator to', decosetting.Value

	context.Write()
		
def get_decorator():
	if decosetting.Value in decorators:
		decorator = decosetting.Value
	else:
		print '* Decorator "'+ decosetting.Value +'" is invalid.'
		decorator = default_decorator()

	return decorator

def set_setting(section, option, value):
	'Sets a setting to ~/.config/fusion-icon'
	configuration.set(section, option, str(value))
	configuration.write(open(config_file, 'w'))

def get_setting(section, option):
	'Retrieves a setting via ~/.config/fusion-icon'
	return configuration.get(section, option)

always_indirect = is_always_indirect()

# Open CompizConfig context
context = compizconfig.Context()
context.Read()
decoplugin = context.Plugins['decoration']
decosetting = compizconfig.Setting(decoplugin, 'command', 0)

# Get installed applications
print "* Searching for installed applications..."
apps_installed = []
for app in apps:
	if system('which ' + app + ' 2>/dev/null') == 0:
		apps_installed.append(app)

# Check if we're using compiz.real wrapper
compiz = 'compiz'
if is_installed('compiz.real'):
	compiz = 'compiz.real'

# Check whether GNOME or KDE or XFCE4 running
kde = gnome = xfce4 = False
if is_running('gnome-session'):
	gnome = True
	print '* Gnome is running'

elif is_running('xfce4-session'):
	xfce4 = True
	print '* XFCE4 is running'
	
elif is_running('dcop'):
	kde = True
	print '* KDE is running'

active_decorator = get_decorator()

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
	# Read the file
	configuration = ConfigParser.ConfigParser()
	configuration.read(config_file)

	# Settings
	active_wm = get_setting('window manager', 'active wm')
	indirect_rendering = int(get_setting('compiz options', 'indirect rendering'))
	loose_binding = int(get_setting('compiz options', 'loose binding'))

except:
	print '* Configuration file (' + config_file + ') invalid'
	if path.exists(config_file):
		config_backup = path.join(config_folder, 'fusion-icon.backup.' + str(int(time())))
		rename(config_file, config_backup)
		print '... backed up to:', config_backup
	print '* Generating new configuration file'
	create_config_file()
	configuration = ConfigParser.ConfigParser()
	configuration.read(config_file)

	# Set default settings
	active_wm = get_setting('window manager', 'active wm')
	indirect_rendering = int(get_setting('compiz options', 'indirect rendering'))
	loose_binding = int(get_setting('compiz options', 'loose binding'))

if not is_installed(active_wm):
	print '* ' + active_wm + ' not installed'
	active_wm = fallback_wm()
	print '... setting to fallback: ' + active_wm

if always_indirect:
	set_setting('compiz options', 'indirect rendering', 1)
	indirect_rendering = 1
	
# Do not restart the wm if it's already running
start_wm_bool = False

for wm in wmlist:
	start_wm_bool = False # Reset for the next round
	if is_running(wm) and wm == active_wm and wm != compiz:
	#always restart compiz since we can't know compiz was started correctly
		start_wm_bool = False
		print '* Active WM is already running'
		break # Break as we've found a running wm
	else:
		start_wm_bool = True

if start_wm_bool:
	start_wm()
