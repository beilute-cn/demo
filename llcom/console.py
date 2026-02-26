import threading
import time
from types import SimpleNamespace
from winpty import PtyProcess
import re


class io:
    def open(self) -> bool:
        pass

    def close(self) -> bool:
        pass

    def is_alive(self) -> bool:
        pass

    def write(self, content: str) -> bool:
        pass

    def read(self) -> str:
        pass


class Serial(io):
    pass


class Process(io):
    def __init__(self, command: str | list) -> None:
        # 接收字符串或列表
        self.command = command
        self.process = None

    def open(self) -> bool:
        if self.process is None:
            self.process = PtyProcess.spawn(argv=self.command, dimensions=(33, 133))
        return self.process is not None

    def close(self) -> bool:
        self.process.close(True)
        self.process = None
        return True

    def is_alive(self) -> bool:
        if self.process is not None:
            return self.process.isalive()
        return False

    def write(self, content: str) -> bool:
        self.process.write(content)
        return True

    def read(self) -> str:
        t = ""
        try:
            t = self.process.read()
        except EOFError:
            # 进程正常结束
            self.close()
        except OSError as e:
            # Windows 错误 10053 等
            if e.winerror == 10053:
                print("Connection aborted by host")
            else:
                print(f"OS error during read: {e}")
            self.close()
        except Exception as e:
            print(f"Unexpected read error: {e}")
            self.close()
        finally:
            return t


class Console:
    def __new__(cls, io: io = None, end=None) -> "Console|None":
        if io is None or not io.open():
            return None
        return super().__new__(cls)

    def __init__(self, io: io = None, end=None) -> "Console | None":
        self.is_running = False
        self.io = io
        self.end = end
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

        if self.io.is_alive():
            if self.io.close():
                pass
            else:
                return False
        else:
            return True

    def _write(self) -> None:
        while self.is_running:
            with self.condition.write:
                if self.buffer.write:
                    data, self.buffer.write = self.buffer.write, ""
                    # print(f"\033[35m{data}\033[0m", end="", flush=True)
                    self.io.write(data)
                else:
                    self.condition.write.wait()

    def _read(self) -> None:
        while self.is_running:
            if self.io.is_alive():
                pass
            else:
                self.close()
                break
            data = self.io.read()
            if data is None or data == "":
                continue
            # print(f"\033[33m{data}\033[0m", end="", flush=True)
            with self.condition.read:
                self.buffer.read += data
                self.condition.read.notify()

    def count(self) -> int:
        return len(self.buffer.read)

    def send(self, content: str) -> bool:
        with self.condition.write:
            if self.end is not None and self.end != "":
                content += self.end
            # print(f"{content=}")
            self.buffer.write += content
            self.condition.write.notify()
        return True

    def receive(self) -> str:
        while True:
            with self.condition.read:
                if self.buffer.read:
                    data, self.buffer.read = self.buffer.read, ""
                    return data
                elif self.is_running:
                    self.condition.read.wait(0.5)
                else:
                    return ""


def test_jlink():
    try:
        jlink = Console(io=Process("jlink -nogui 1"), end="\r\n")

        while not re.fullmatch(r"[\s\S]*J-Link>", jlink.buffer.read):
            time.sleep(0.5)
        print(f"{jlink.receive()=}", end="", flush=True)

        commands = [
            # "?",
            "connect",
            "KW47B42ZB7_M33_0",  # device
            "S",
            "4000",  # speed
            "w4 40021000 1234abcd",  # register file
            "mem32 40021000 1",
            "erase",
            "w4 40021000 abcd1234",
            "mem32 40021000 1",
            "quit",
        ]

        for cmd in commands:
            jlink.send(cmd)
            while jlink.io.is_alive() and not re.fullmatch(
                r"[\s\S]*>", jlink.buffer.read
            ):
                time.sleep(0.5)
            print(f"{jlink.receive()=}", end="", flush=True)

    except KeyboardInterrupt as e:
        print("Process interrupted by user")
    finally:
        print("Process terminated")
        jlink.close()


def test_gdb():
    try:
        gdb = Console(
            io=Process("JLinkGDBServerCL -if SWD -device KW47B42ZB7 -nogui 1")
        )

        while gdb.io.is_alive():
            print(f"{gdb.receive()}", end="", flush=True)

    except KeyboardInterrupt as e:
        print("Process interrupted by user")
    finally:
        print("Process terminated")
        gdb.close()


if __name__ == "__main__":
    # test_jlink()
    while True:
        test_gdb()
