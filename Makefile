# Makefile for Compiz Fusion Icon
# Written by: crdlb <christopherw@verizon.net>

prefix = /usr
dirs := 22x22 24x24 32x32 48x48
#qt3 not installed by default as it is broken
frontends := gtk qt4

help:
	$(info * type 'sudo make install' to install fusion-icon to /usr)
	$(info ... or use 'sudo make prefix=/path install' to specify a different prefix.)
	$(info ... by default, all frontends are installed (gtk, qt3, and qt4)[qt3 is temporarily removed due to brokenness]. To install with only gtk (for example), use 'sudo make frontends=gtk install' )
	@echo -n
	
install:
	mkdir -p $(DESTDIR)$(prefix)/share/fusion-icon/
	install src/libfusionicon.py $(DESTDIR)$(prefix)/share/fusion-icon/
	for frontend in $(frontends); do install src/fusion-icon-$$frontend.py $(DESTDIR)$(prefix)/share/fusion-icon/; done
	mkdir -p $(DESTDIR)$(prefix)/bin/
	install src/fusion-icon $(DESTDIR)$(prefix)/bin
	for dir in $(dirs); do mkdir -p $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/ && install images/$$dir/fusion-icon.png $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/; done
	mkdir -p $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/
	install images/scalable/fusion-icon.svg $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/ 
	if [[ 'which gtk-update-icon-cache 2>&1>/dev/null' && -f $(DESTDIR)$(prefix)/share/icons/hicolor/index.theme ]]; then gtk-update-icon-cache $(DESTDIR)$(prefix)/share/icons/hicolor; fi
	mkdir -p $(DESTDIR)$(prefix)/share/applications
	install fusion-icon.desktop $(DESTDIR)$(prefix)/share/applications/fusion-icon.desktop
	
uninstall:
	-rm -r $(DESTDIR)$(prefix)/share/fusion-icon/ 
	-rm $(DESTDIR)$(prefix)/bin/fusion-icon 
	-for dir in $(dirs); do rm $(DESTDIR)$(prefix)/share/icons/hicolor/$$dir/apps/fusion-icon.png; done
	-rm $(DESTDIR)$(prefix)/share/icons/hicolor/scalable/apps/fusion-icon.svg
	-rm $(DESTDIR)$(prefix)/share/applications/fusion-icon.desktop
