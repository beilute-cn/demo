#include <stdio.h>

#define print(...) printf(__VA_ARGS__)

int main(void) {
	print("start\r\n");

	print("end\r\n");
	return 0;
}
a
