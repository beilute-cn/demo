# .DEFAULT_GOAL := test

hello:
	echo "hello from /coverage/makefile"

report:
	gcc -fprofile-arcs -ftest-coverage -fPIC -O0 function.c main.c -o program
	program
	gcovr --html --html-details index.html
	
# --no-markers
clean:
	del *.gcda
	del *.gcno
	del *.html
	del *.exe
	del *.js
	del *.css
