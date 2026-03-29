import subprocess
import time


class Process:
    def __init__(self, command: str | list) -> None:
        self.command = command if isinstance(command, list) else [command]
        self.process = None

    def open(self) -> bool:
        if self.process is None:
            self.process = subprocess.Popen(
                args=self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        return self.process is not None

    def close(self) -> bool:
        # communicate() -> poll()
        # timeout -> kill()
        self.process.kill()
        self.process = None
        return True

    def write(self, content: str) -> bool:
        print(f"{content=}")
        self.process.stdin.write(content)
        self.process.stdin.flush()
        return True

    def read(self) -> str:
        if False:
            for line in self.process.stdout:
                print(f"{line}", end="")
        else:
            try:
                while True:
                    data = self.process.stdout.readline()
                    print(f"{data}", end="", flush=True)
            except KeyboardInterrupt as e:
                pass
            finally:
                pass
        return "test text"


def f1():
    try:
        # 方式1: 基本用法 - 捕获所有流
        process = subprocess.Popen(
            args=["jlink"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 发送 'q' 到 jlink 的标准输入
        process.stdin.write("q\n")
        process.stdin.flush()

        for line in process.stdout:
            print(f"{line}", end="")
    finally:
        pass


def f2():
    try:
        p = Process("jlink")
        p.open()
        p.write("q\n")
        print(f"{ p.read()}")

    finally:
        pass


try:
    f1()
    print("=" * 50)
    f2()
finally:
    pass
