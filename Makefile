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
	install src/libfusionicon.py $(DESTDIR)$(prefix)/share/fusion-icon/
	for frontend in $(frontends); do install src/fusion-icon-$$frontend.py $(DESTDIR)$(prefix)/share/fusion-icon/; done
	mkdir -p $(DESTDIR)$(prefix)/bin/
	install src/fusion-icon $(DESTDIR)$(prefix)/bin
	for dir in $(dirs); do mkdir -p $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/ && install images/$$dir/fusion-icon.png $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/; done
	mkdir -p $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/
	install images/scalable/fusion-icon.svg $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/ 
	
uninstall:
	-rm -r $(DESTDIR)$(prefix)/share/fusion-icon/ 
	-rm $(DESTDIR)$(prefix)/bin/fusion-icon 
	-for dir in $(dirs); do rm $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/fusion-icon.png; done
	-rm $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/fusion-icon.svg

