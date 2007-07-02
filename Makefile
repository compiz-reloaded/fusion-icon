# Makefile for Compiz Fusion Icon
# Written by: crdlb <christopherw@verizon.net>

# Default installation directory (from prefix in python)
TARGET=/usr

# Make options
build:
	./setup.py build
install:
	./setup.py install
clean:
	./setup.py clean
uninstall:
	rm $(TARGET)/bin/fusion-icon
	rm $(TARGET)/share/icons/hicolor/22x22/apps/fusion-icon.png
	rm $(TARGET)/share/icons/hicolor/48x48/apps/fusion-icon.png
	rm $(TARGET)/share/icons/hicolor/scalable/apps/fusion-icon.svg

