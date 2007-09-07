PREFIX = '/usr'
DESTDIR = '/'
interfaces = 'gtk qt4'

all:
	@python setup.py build

install:
	@interfaces=${interfaces} python setup.py install --prefix=${PREFIX} --root=${DESTDIR}

uninstall:
	@python setup.py uninstall

clean:
	rm -rf build/

