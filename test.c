#include <stdio.h>

int main(void)
{
    char buffer[100];
    for (int i = 0; i < 5; ++i)
    {
        printf("i=%d\n", i);
    }

    fgets(buffer, sizeof(buffer), stdin);
    printf("buffer=%s\n", buffer);

    for (int i = 0; i < 5; ++i)
    {
        printf("i=%d\n", i);
    }
    return 0;
}
