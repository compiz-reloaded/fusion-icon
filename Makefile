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
	rm $(TARGET)/share/pixmaps/ct-icon.svg
	rm $(TARGET)/bin/compiz-fusion-icon
