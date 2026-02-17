import threading
import time
import subprocess
from types import SimpleNamespace
import sys


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
        self.is_open = False

    def _peek_pipe(self, handle):
        """使用 Windows API 检查管道中是否有数据"""
        if sys.platform != 'win32':
            return 0
        
        try:
            import ctypes
            from ctypes import wintypes
            
            # 获取 kernel32.dll
            kernel32 = ctypes.windll.kernel32
            
            # PeekNamedPipe 函数
            # BOOL PeekNamedPipe(
            #   HANDLE  hNamedPipe,
            #   LPVOID  lpBuffer,
            #   DWORD   nBufferSize,
            #   LPDWORD lpBytesRead,
            #   LPDWORD lpTotalBytesAvail,
            #   LPDWORD lpBytesLeftThisMessage
            # );
            
            bytes_avail = wintypes.DWORD()
            result = kernel32.PeekNamedPipe(
                handle,
                None,
                0,
                None,
                ctypes.byref(bytes_avail),
                None
            )
            
            if result:
                return bytes_avail.value
            return 0
        except Exception as e:
            print(f"\033[31m[peek error] {e}\033[0m")
            return 0

    def open(self) -> bool:
        if self.process is None:
            try:
                self.process = subprocess.Popen(
                    args=self.command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=0,  # 无缓冲
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
                self.is_open = True
                return True
            except Exception as e:
                print(f"\033[31m[Process open error] {e}\033[0m")
                return False
        return self.process is not None

    def close(self) -> bool:
        self.is_open = False
        
        if self.process:
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait()
            except Exception as e:
                print(f"\033[31m[Process close error] {e}\033[0m")
            finally:
                self.process = None
        
        return True

    def write(self, content: str) -> bool:
        if self.process and self.process.stdin and self.is_open:
            try:
                self.process.stdin.write(content)
                self.process.stdin.flush()
                return True
            except (BrokenPipeError, OSError, ValueError) as e:
                print(f"\033[31m[Process write error] {e}\033[0m")
                return False
        return False

    def read(self) -> str:
        """非阻塞读取，使用 Windows API 检查可用数据"""
        if not self.process or not self.is_open:
            return ""
        
        data = ""
        
        try:
            # 获取 stdout 的文件句柄
            import msvcrt
            stdout_handle = msvcrt.get_osfhandle(self.process.stdout.fileno())
            stderr_handle = msvcrt.get_osfhandle(self.process.stderr.fileno())
            
            # 检查 stdout 是否有数据
            stdout_avail = self._peek_pipe(stdout_handle)
            if stdout_avail > 0:
                # 读取可用的字符数
                chunk = self.process.stdout.read(stdout_avail)
                if chunk:
                    data += chunk
            
            # 检查 stderr 是否有数据
            stderr_avail = self._peek_pipe(stderr_handle)
            if stderr_avail > 0:
                chunk = self.process.stderr.read(stderr_avail)
                if chunk:
                    print(f"\033[34m[stderr] {chunk}\033[0m", end="", flush=True)
                    data += chunk
            
        except Exception as e:
            print(f"\033[31m[Process read error] {e}\033[0m")
        
        return data


class Console:

    def __new__(cls, io: io = None) -> "Console|None":
        if io is None:
            return None
        if not io.open():
            return None
        return super().__new__(cls)

    def __init__(self, io: io = None) -> None:
        self.is_running = False
        self.io = io
        self.thread = SimpleNamespace(write=None, read=None)
        self.condition = SimpleNamespace(write=None, read=None)
        self.buffer = SimpleNamespace(write="", read="")
        self.open()

    def open(self) -> bool:
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
        time.sleep(0.2)  # 等待线程退出
        if self.io:
            return self.io.close()
        return True

    def _write(self) -> None:
        while self.is_running:
            with self.condition.write:
                if self.buffer.write:
                    data, self.buffer.write = self.buffer.write, ""
                    print(f"\033[35m[send] {repr(data)}\033[0m", flush=True)
                    self.io.write(data)
                else:
                    self.condition.write.wait(timeout=0.1)

    def _read(self) -> None:
        while self.is_running:
            try:
                data = self.io.read()
                if data:
                    print(f"\033[33m[recv] {repr(data)}\033[0m", flush=True)
                    with self.condition.read:
                        self.buffer.read += data
                        self.condition.read.notify()
                else:
                    time.sleep(0.01)  # 避免空转占用 CPU
            except Exception as e:
                print(f"\033[31m[_read error] {e}\033[0m")
                time.sleep(0.1)

    def count(self) -> int:
        with self.condition.read:
            return len(self.buffer.read)

    def send(self, content: str) -> bool:
        with self.condition.write:
            self.buffer.write += content
            self.condition.write.notify()
        return True

    def receive(self, timeout: float = None) -> str:
        """接收数据，支持超时"""
        with self.condition.read:
            if self.buffer.read:
                data, self.buffer.read = self.buffer.read, ""
                return data
            else:
                self.condition.read.wait(timeout=timeout)
                if self.buffer.read:
                    data, self.buffer.read = self.buffer.read, ""
                    return data
                return ""


if __name__ == "__main__":
    try:
        # 测试用例
        p = Process(["python", "-u", "-c", "import time; [print(f'line {i}', flush=True) or time.sleep(1) for i in range(10)]"])
        c = Console(p)
        
        if c:
            print("Console started, waiting for output...")
            time.sleep(15)
            
            # 获取所有接收到的数据
            final_data = c.receive(timeout=1)
            print(f"\n\033[32m[Final data] {repr(final_data)}\033[0m")
    except KeyboardInterrupt:
        print("\n\033[33m[Interrupted]\033[0m")
    finally:
        if 'c' in locals() and c:
            c.close()
            print("\033[36m[Console closed]\033[0m")
