.DEFAULT_GOAL := coverage

.PHONY: hello coverage

make := mingw32-make.exe


hello:
	cls
	echo "hello from /makefile"

coverage:
	cls
	$(make) -C coverage report
