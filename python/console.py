import threading
from types import SimpleNamespace

from io import io


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
