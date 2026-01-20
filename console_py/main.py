import ctypes
from ctypes import wintypes

from _input_record import _input_record

kernel = ctypes.windll.kernel32

# 定义函数原型
if True:
    if True:
        # GetStdHandle
        kernel.GetStdHandle.argtypes = [wintypes.DWORD]
        kernel.GetStdHandle.restype = wintypes.HANDLE

    # ReadConsole 字符
    test_ReadConsole = False  # WA
    # ReadConsoleInput 事件
    test_ReadConsoleInput = True  # WA
    # ReadConsoleInputEx
    # ReadConsoleOutput
    # ReadConsoleOutputAttribute
    # ReadConsoleOutputCharacter (读取控制台输出字符)

    # ReadConsole 在 Windows API 中实际上是一个宏，真实的函数名是：
    # ReadConsoleA - ANSI 版本
    # ReadConsoleW - Unicode 版本
    # 需要使用 ReadConsoleW 或 ReadConsoleA，而不是 ReadConsole。

    if True:
        # ReadConsoleA
        kernel.ReadConsoleA.argtypes = [
            wintypes.HANDLE,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPVOID,
        ]
        kernel.ReadConsoleA.restype = wintypes.BOOL

    if True:
        # ReadConsoleInputA
        kernel.ReadConsoleInputA.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(_input_record),
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
        ]
        kernel.ReadConsoleInputA.restype = wintypes.BOOL


stdin = kernel.GetStdHandle(-10)

if test_ReadConsole:
    size = wintypes.DWORD(20)
    buffer = ctypes.create_string_buffer(size.value)
    length = wintypes.DWORD()

    while True:
        ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
        # length.value = 0
        flag = kernel.ReadConsoleA(
            stdin,
            buffer,
            size,
            ctypes.byref(length),
            None,
        )
        print(f"返回值：{flag}，长度：{length}，内容：{buffer.value}")


# 部分快捷键被vscode拦截，Ctrl + Shift + 2 可以
# 大写锁定，数字锁定，滚动锁定等状态只在wt有效，是种状态
# 仅按控制键，在wt可以检测到
# vscode在，输入后，即认为全部释放
# wt在实际释放时，才接收到
# 总是偶数

# X10   9   最大94（126-32），Alt/Shift
# SGR   1006

# 1000
# 1001 高亮
# 1002 拖拽
# 1003 移动


def parse(records, length):
    for i in range(length):
        records[i].parse()
        # print(records[i])


if test_ReadConsoleInput:
    try:
        n = [1006, 1002]

        for i in n:
            print(f"\033[?{i}h", end="", flush=True)

        size = wintypes.DWORD(10)
        buffer = (_input_record * size.value)()
        length = wintypes.DWORD()
        while True:
            # ctypes.memset(ctypes.addressof(buffer), 0, ctypes.sizeof(buffer))
            flag = kernel.ReadConsoleInputA(
                stdin,
                buffer,
                size,
                ctypes.byref(length),
            )

            # print(f"返回值：{flag}, 长度：{length}，内容：")
            parse(buffer, length.value)

    except KeyboardInterrupt:
        for i in n:
            print(f"\033[?{i}l", end="", flush=True)
        print(f"\033[0m", end="", flush=True)
        print("KeyboardInterrupt")
