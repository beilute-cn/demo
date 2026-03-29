# .DEFAULT_GOAL := coverage

.PHONY: hello coverage clean

make := mingw32-make.exe


hello:
	echo "hello from /makefile"

coverage:
	$(make) -C coverage report

clean:
	$(make) -C coverage clean