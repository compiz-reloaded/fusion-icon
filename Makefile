PREFIX = '/usr'
DESTDIR = '/'
interfaces = 'qt gtk'

all:
	@python setup.py build

install:
	@python setup.py install --prefix=${PREFIX} --root=${DESTDIR}

uninstall:
	@python setup.py uninstall

clean:
	rm -rf build/

