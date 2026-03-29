from winpty import PtyProcess

from io import io


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
