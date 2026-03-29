# .DEFAULT_GOAL := test

hello:
	cls
	echo "hello from /coverage/makefile"

report:
	cls
	gcc -fprofile-arcs -ftest-coverage -fPIC -O0 function.c main.c -o program
	program
	gcovr --html --html-details index.html
	
# --no-markers