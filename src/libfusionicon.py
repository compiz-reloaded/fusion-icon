#!/usr/bin/env python
# Author(s): crdlb, nesl247
import ConfigParser, compizconfig, commands, os, subprocess, time

# Define variables
fglrx_locations = ('/usr/lib/fglrx/libGL.so.1.2.xlibmesa', '/opt/mesa-xgl/lib/libGL.so.1.2')

apps = ('compiz.real', 'ccsm', 'compiz', 'gtk-window-decorator', 'kde-window-decorator', 'emerald', 'metacity', 'kwin', 'xfwm4') 
wmlist = ('compiz', 'xfwm4', 'kwin', 'metacity')

emerald = 'emerald --replace'
kwd = 'kde-window-deocrator --replace'
gwd = 'gtk-window-decorator --replace'
decorators = (gwd, kwd, emerald)


# Defining functions
def is_running(app):
	if os.system('pgrep ' + app + ' 1>/dev/null') == 0:
		return True
	else:
		return False

def is_installed(app):
	global app_is_installed
	return app in apps_installed

def default_decorator():
	'Find the default decorator to use'

	decorator = ''
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

	if decorator != '':
		print '... choosing', decorator, 'as default decorator'
	else:
		print '*** Warning: no decorator found'

	return decorator

def create_config_file():
	default_config = open(config_file, 'w')
	default_config.write('[compiz options]\nindirect rendering = 0\nloose binding = 0\n\n[window manager]\nactive wm = %s' %(compiz))
	default_config.close()

def fallback_wm():
	'Return a fallback window manager'

	if is_installed('kwin') and kde and not gnome and not xfce4:
		wm = 'kwin'

	elif is_installed('metacity') and gnome and not kde and not xfce4:
		wm = 'metacity'

	elif is_installed('xfwm4') and not kde and not gnome and xfce4:
		wm = 'xfwm4'

	else:
		wm = ''

	set_setting('window manager', 'active wm', wm)
	return wm

def env_intel():
	'Determines if we are using intel'

	if not commands.getoutput('xvinfo 2>/dev/null|grep Intel') == '':
		print '* Intel found, exporting: INTEL_BATCH=1'
		return 'INTEL_BATCH=1 '
	else:
		return ''

def is_always_indirect():
	'Determines if we are always using indirect rendering'

	if int(commands.getoutput('glxinfo 2>/dev/null | grep GLX_EXT_texture_from_pixmap -c')) < 3:
		if int(commands.getoutput('LIBGL_ALWAYS_INDIRECT=1 glxinfo 2>/dev/null | grep GLX_EXT_texture_from_pixmap -c')) == 3:
			return True

	else:
		return False
	
def env_indirect():
	'Determines if we are using indirect rendering (wrapping is_always_indirect() so that the check can be used more than once without printing the status text)'

	if is_always_indirect():
		print '* No GLX_EXT_texture_from_pixmap present with direct rendering context'
		print '... present with indirect rendering, exporting: LIBGL_ALWAYS_INDIRECT=1'
		return 'LIBGL_ALWAYS_INDIRECT=1 '
	else:
		return ''

def env_fglrx():
	'Determines if we are using fglrx'

	for location in fglrx_locations:
		if os.path.exists(location):
			print '* fglrx found, exporting: LD_PRELOAD=' + location + ' '
			return 'LD_PRELOAD=' + location + ' '
	# We've not found anything
	return ''
	
def env_nvidia():
	'Determines if we are using nvidia'

	if not commands.getoutput('xdpyinfo 2>/dev/null|grep NV-GLX') == '':
		print '* nvidia found, exporting: __GL_YIELD="NOTHING" '
		return '__GL_YIELD="NOTHING" '
	else:
		return ''
	
def get_env():
	return env_intel() + env_indirect() + env_fglrx() + env_nvidia()

def start_wm():
	active_wm = get_setting('window manager', 'active wm')
	global old_wm
	# Ugly hack follows because xfwm4 is evil:
	# 1) we kill the old wm if compiz needs to replace xfwm4
	#    (so that compiz doesn't fail with a composite manager already running error)
	# 2) we kill the old wm if xfwm4 needs to start since it apparently lacks a '--replace' switch
	print old_wm
	if (old_wm == 'xfwm4' and active_wm == compiz) or active_wm == 'xfwm4':
		print '* killing all WMs to work around xfwm4\'s brokenness'
		os.system('killall ' + ' '.join(wmlist) + ' 2>/dev/null')
		time.sleep(0.5)

	if active_wm == compiz:
		start_compiz()

	else:
		print "* Starting:", active_wm
		subprocess.Popen(active_wm + ' --replace', shell=True)

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
	subprocess.Popen(run_compiz, shell=True)

def set_old_wm():
	'Sets global old_wm variable to the current window manager'
	
	global old_wm
	old_wm = get_setting('window manager', 'active wm')

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


# Open CompizConfig context
context = compizconfig.Context()
context.Read()
decoplugin = context.Plugins['decoration']
decosetting = decoplugin.Display['command']

# Get installed applications
print "* Searching for installed applications..."
apps_installed = []
for app in apps:
	if os.system('which ' + app + ' 2>/dev/null') == 0:
		apps_installed.append(app)

# Check if we're using compiz.real wrapper
compiz = ''
if is_installed('compiz.real'):
	compiz = 'compiz.real'
elif is_installed('compiz'):
	compiz = 'compiz'
	
# Check whether GNOME or KDE or XFCE4 running
kde = gnome = xfce4 = False
if is_running('gnome-session'):
	gnome = True
	print '* Gnome is running'

elif is_running('xfce4-session'):
	xfce4 = True
	print '* XFCE4 is running'
	
elif is_running('kdeinit') or is_running('startkde'):
	kde = True
	print '* KDE is running'

# Variables
active_decorator = get_decorator()
old_wm = '' #set to empty string so that initial start_wm() doesn't fail
config_folder = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.environ.get('HOME'), '.config'))  
config_file = os.path.join(config_folder, 'fusion-icon')

# Configuration file setup
if not os.path.exists(config_folder):
	os.mkdir(config_folder)
	create_config_file()

elif not os.path.exists(config_file):
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
	if os.path.exists(config_file):
		config_backup = os.path.join(config_folder, 'fusion-icon.backup.' + str(int(time.time())))
		os.rename(config_file, config_backup)
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

#Set True if using Xorg AIGLX since the '--indirect-rendering' option has no effect in that situation.
always_indirect = is_always_indirect()

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
