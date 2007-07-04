# Makefile for Compiz Fusion Icon
# Written by: crdlb <christopherw@verizon.net>

prefix = /usr
dirs := 22x22 24x24 32x32 48x48
frontends := gtk qt3 qt4

help:
	$(info * type 'sudo make install' to install fusion-icon to /usr)
	$(info ... or use 'sudo make prefix=/path install' to specify a different prefix.)
	$(info ... by default, all frontends are installed (gtk, qt3, and qt4). To install with only gtk (for example), use 'sudo make frontends=gtk install' )

install:
	mkdir -p $(DESTDIR)$(prefix)/share/fusion-icon/
	install -t $(DESTDIR)$(prefix)/share/fusion-icon/ src/libfusionicon.py
	for frontend in $(frontends); do install -t $(DESTDIR)$(prefix)/share/fusion-icon/ src/fusion-icon-$$frontend.py; done
	mkdir -p $(DESTDIR)$(prefix)/bin/
	install -t $(DESTDIR)$(prefix)/bin src/fusion-icon
	
	for dir in $(dirs); do mkdir -p $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/ && install -t $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/ images/$$dir/fusion-icon.png; done
	mkdir -p $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/
	install -t $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/ images/scalable/fusion-icon.svg
	
uninstall:
	-rm -r $(DESTDIR)$(prefix)/share/fusion-icon/ 
	-rm $(DESTDIR)$(prefix)/bin/fusion-icon 
	-for dir in $(dirs); do rm $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/fusion-icon.png; done
	-rm $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/fusion-icon.svg

