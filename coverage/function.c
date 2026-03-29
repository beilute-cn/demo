#include "function.h"

#include <stdio.h>

// 正常调用
int function(int n)
{
    int r = 0;
    for (int i = 0; i < n; ++i)
    {
        r += i;
    }
    return r;
}

// 测试排除行、分支
void exclude(void)
{
    int i = 0;
    if (i == 7)
    {
        i = __LINE__;
        i = __LINE__; /* GCOVR_EXCL_LINE */
        i = __LINE__;
    }

    if (i == 9) /* GCOVR_EXCL_BR_LINE */
    {
        i = __LINE__;
    }
    else
    {
        i = __LINE__;
    }
}

// 测试排除函数
void exclude_function(void) /* GCOVR_EXCL_FUNCTION */
{
    int i = __LINE__;
    i = __LINE__;
}
