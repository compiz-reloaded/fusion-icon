# Makefile for Compiz Fusion Icon
# Written by: crdlb <christopherw@verizon.net>

prefix = /usr
dirs := 22x22 24x24 32x32 48x48 scalable
frontends := gtk qt3 qt4

help:
	$(info * type 'sudo make install' to install fusion-icon to /usr)
	$(info ... or use 'sudo make prefix=/path install' to specify a different prefix.)
	$(info ... by default, all frontends are installed (gtk, qt3, and qt4). To install with only gtk (for example), use 'sudo make frontends=gtk install' )

install:
	mkdir -p $(prefix)/share/fusion-icon/
	install -t $(prefix)/share/fusion-icon/ src/libfusionicon.py
	for frontend in $(frontends); do install -t $(prefix)/share/fusion-icon/ src/fusion-icon-$$frontend.py; done
	mkdir -p $(prefix)/bin/
	install -t $(prefix)/bin/ src/fusion-icon
	for dir in $(dirs); do mkdir -p $(prefix)/share/icons/hicolor/$$dir/apps/ && install -t $(prefix)/share/icons/hicolor/$$dir/apps/ images/$$dir/fusion-icon.*; done
	
uninstall:
	-rm -r $(prefix)/share/fusion-icon/ 
	-rm $(prefix)/bin/fusion-icon 
	-for dir in $(dirs); do rm $(prefix)/share/icons/hicolor/$$dir/apps/fusion-icon.*; done

