import threading
import time
import subprocess
from types import SimpleNamespace

from winpty import PtyProcess
import time


import ctypes
from ctypes import wintypes
import sys

import re

"""
BOOL PeekNamedPipe(
  HANDLE  hNamedPipe,              // 管道句柄
  LPVOID  lpBuffer,                // 接收数据的缓冲区（可为 NULL）
  DWORD   nBufferSize,             // 缓冲区大小
  LPDWORD lpBytesRead,             // 实际读取的字节数（可为 NULL）
  LPDWORD lpTotalBytesAvail,       // 管道中可用的总字节数（可为 NULL）
  LPDWORD lpBytesLeftThisMessage   // 当前消息剩余字节数（可为 NULL）
);
"""

import msvcrt


def peek_pipe_simple(handle):
    """简单版本：只获取可用字节数"""
    if sys.platform != "win32":
        return 0

    kernel32 = ctypes.windll.kernel32
    bytes_avail = wintypes.DWORD()

    result = kernel32.PeekNamedPipe(
        handle,  # 管道句柄
        None,  # 不读取数据
        0,  # 缓冲区大小为 0
        None,  # 不需要已读字节数
        ctypes.byref(bytes_avail),  # 获取可用字节数
        None,  # 不需要剩余消息字节数
    )

    if result:
        return bytes_avail.value
    else:
        error = kernel32.GetLastError()
        print(f"Error: {error}")
        return 0


class io:
    def open(self) -> bool:
        pass

    def close(self) -> bool:
        pass

    def write(self, content: str) -> bool:
        pass

    def read(self) -> str:
        pass


class Serial(io):
    pass


class Process(io):
    def __init__(self, command: str | list) -> None:
        self.command = command if isinstance(command, list) else [command]
        self.process = None

    def open(self) -> bool:
        if self.process is None:
            self.process = PtyProcess.spawn(argv=self.command, dimensions=(33, 133))
        return self.process is not None

    def close(self) -> bool:
        # communicate() -> poll()
        # timeout -> kill()
        # self.process.kill()
        # self.process = None

        # TODO close -> None
        return True

    def write(self, content: str) -> bool:
        # self.process.stdin.write(content)
        # self.process.stdin.flush()
        self.process.write(content)
        return True

    # TODO win32 peek
    def read(self) -> str:
        # n = peek_pipe_simple(msvcrt.get_osfhandle(self.process.stdout.fileno()))
        # if n:
        # print(f"管道字符数：{n}")
        # n = 100
        # return self.process.stdout.read(n)
        return self.process.read()


def read_util(process: Process, pattern: str | re.Pattern[str]) -> str:
    r = []
    while True:
        t = process.read()
        print(f"{t}", end="", flush=True)
        r.append(t)
        if re.fullmatch(pattern, t):
            break
    return "".join(r)


def exec(process: Process, command: str, end: str | re.Pattern[str]) -> str:
    process.write(command)
    return read_util(process, end)


if True:
    try:
        p = Process("jlink")
        p.open()
        read_util(p, r"[\s\S]*J-Link>")
        exec(p, "?\r\n", r"[\s\S]*J-Link>")
        exec(p, "connect\r\n", r"[\s\S]*Device>")
        exec(p, "\r\n", r"[\s\S]*TIF>")
        exec(p, "S\r\n", r"[\s\S]*Speed>")
        exec(p, "\r\n", r"[\s\S]*J-Link>")
        exec(p, "erase\r\n", r"[\s\S]*J-Link>")
        exec(p, "quit\r\n", r"[\s\S]*J-Link>")

    except KeyboardInterrupt as e:
        p.close()
    finally:
        print("")
        sys.exit(-1)

if True:
    try:
        # 启动 JLink
        print("启动 JLink...")
        jlink = PtyProcess.spawn("jlink")

        # 等待初始化
        time.sleep(0.5)

        for i in range(10):
            # time.sleep(0.01)
            t = jlink.read()
            if t:
                print(f"[{i}] > {t}")
            else:
                break
        sys.exit(-1)

        # 发送命令
        print("\n发送命令: ?")
        jlink.write("?\r\n")

        # 读取响应
        time.sleep(0.2)
        response = jlink.read()
        print(response)

        # # 连接设备
        # print("\n连接设备...")
        # jlink.write("connect\r\n")
        # time.sleep(0.1)
        # print(jlink.read())

        # # 选择设备
        # jlink.write("STM32F103C8\r\n")
        # time.sleep(0.1)
        # print(jlink.read())

        # # 选择接口
        # jlink.write("S\r\n")  # SWD
        # time.sleep(0.1)
        # print(jlink.read())

        # # 速度
        # jlink.write("4000\r\n")
        # time.sleep(0.1)
        # print(jlink.read())

        # 退出
        jlink.write("exit\r\n")
        time.sleep(0.1)
        print(jlink.read())

    except Exception as e:
        print(f"错误: {e}")
    finally:
        jlink.close()

    sys.exit(-1)


class Console:

    def __new__(cls, io: io = None) -> "Console|None":
        if io is None or not io.open():
            return None
        return super().__new__(cls)

    def __init__(self, io: io = None) -> "Console | None":
        self.is_running = False
        self.io = io
        self.thread = SimpleNamespace(write=None, read=None)
        self.condition = SimpleNamespace(write=None, read=None)
        self.buffer = SimpleNamespace(write="", read="")
        self.open()

    def open(self) -> bool:

        if not self.io.open():
            return False

        self.is_running = True

        self.thread.write = threading.Thread(target=self._write, daemon=True)
        self.thread.read = threading.Thread(target=self._read, daemon=True)

        self.condition.write = threading.Condition()
        self.condition.read = threading.Condition()

        self.buffer.write = ""
        self.buffer.read = ""

        self.thread.write.start()
        self.thread.read.start()

        return True

    def close(self) -> bool:
        self.is_running = False
        if not self.io.close():
            return False
        return True

    def _write(self) -> None:
        while self.is_running:
            with self.condition.write:
                if self.buffer.write:
                    data, self.buffer.write = self.buffer.write, ""
                    print(f"\033[35m{data}\033[0m", end="", flush=True)
                    self.io.write(data)
                else:
                    self.condition.write.wait()

    def _read(self) -> None:
        while self.is_running:
            data = self.io.read()
            print(f"\033[33m{data}\033[0m", end="", flush=True)
            with self.condition.read:
                self.buffer.read += data
                self.condition.read.notify()

    def count(self) -> int:
        return len(self.buffer.read)

    def send(self, content: str) -> bool:
        with self.condition.write:
            self.buffer.write += content
            self.condition.write.notify()
        return True

    def receive(self) -> str:
        while True:
            with self.condition.read:
                if self.buffer.read:
                    data, self.buffer.read = self.buffer.read, ""
                    return data
                else:
                    self.condition.read.wait()


# try:
# p = Process("jlink")
# c = Console(p)
# while True:
# print("=" * 50)
# c.send("erase\n")
# time.sleep(5)
# finally:
# c.close()
