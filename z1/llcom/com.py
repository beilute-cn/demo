"""
常见的 noqa 代码
代码	说明
# noqa	忽略该行所有警告
# noqa: E501	忽略"行太长"警告
# noqa: F401	忽略"导入但未使用"警告
# noqa: E401	忽略"多个导入在一行"警告
对比总结
注释	        作用范围	主要工具	      用途
# fmt: off/on	多行代码块	Black	         禁用格式化
# fmt: skip     单行	    Black       	禁用格式化
# noqa          单行	    flake8/pylint	忽略代码检查警告
"""

import threading
import serial.tools.list_ports
import time
import string
from types import SimpleNamespace
import sys
from enum import Enum, auto
import re


"""
class SerialBase(io.RawIOBase):

serial.Serial(
    port=None,                   # 0. 串口名称
    baudrate=9600,               # 1. 波特率
    bytesize=EIGHTBITS,          # 2. 数据位
    parity=PARITY_NONE,          # 3. 校验位
    stopbits=STOPBITS_ONE,       # 4. 停止位
    timeout=None,                # 5. 读超时
    xonxoff=False,               # 6. 软件流控
    rtscts=False,                # 7. 硬件流控 RTS/CTS
    write_timeout=None,          # 8. 写超时
    dsrdtr=False,                # 9. 硬件流控 DSR/DTR
    inter_byte_timeout=None,     # 10. 字节间超时
    exclusive=None               # 11. 独占模式
)

"""
# 调用more命令
# 缓冲大小和数据字节数
# help(serial.Serial)
# help(serial.Serial.__init__)


# 查看函数签名
# sig = inspect.signature(serial.Serial.__init__)
# print(f"{sig=}")

# 查看参数列表
# for param_name, param in sig.parameters.items():
# print(f"{param_name}: {param.default}")

# python -c "import serial; print(serial.__file__)"


class Com:

    def __init__(self, port):
        self.port = port
        self.stop = False
        self.thread = None
        self.thread = SimpleNamespace(write=None, read=None)
        self.serial = None
        self.data = SimpleNamespace(write="", read="")

    def __eq__(self, other):
        return self.port == other.port

    class message_type(Enum):
        input = auto()
        output = auto()
        info = auto()

    def print(self, type: message_type, message: str):
        match (type):
            case Com.message_type.input:
                print(f"\033[33m[{self.port}] \033[32m-> {message}\033[0m")
            case Com.message_type.output:
                print(f"\033[33m[{self.port}] \033[34m<- {message}\033[0m")
            case Com.message_type.info:
                print(f"\033[33m[{self.port}] \033[36m:: {message}\033[0m")

    def connect(self):
        try:
            self.serial = serial.Serial(port=self.port, baudrate=115200, timeout=1)
            self.stop = False
            self.thread.write = threading.Thread(target=self.write, daemon=True)
            self.thread.read = threading.Thread(target=self.read, daemon=True)
            self.thread.write.start()
            self.thread.read.start()
            self.print(Com.message_type.info, f"连接成功")
            return True
        except serial.SerialException as e:
            self.print(Com.message_type.info, f"串口异常: {e}")
            self.serial = None
            return False
        except Exception as e:
            self.print(Com.message_type.info, f"异常: {e}")
            self.serial = None
            return False

    def disconnect(self):
        if self.serial is None:
            return
        self.stop = True
        while self.thread.write is not None or self.thread.read is not None:
            time.sleep(0.1)

        try:
            self.serial.close()
            self.print(Com.message_type.info, f"已断开")
        except Exception as e:
            self.print(Com.message_type.info, f"异常：{e}")

    def write(self):
        while not self.stop:
            try:
                if self.data.write == "":
                    continue
                text = self.data.write
                self.data.write = ""
                self.serial.write(text.encode("utf-8"))
                self.print(Com.message_type.output, f"{text}")
            except serial.SerialException as e:
                self.print(Com.message_type.info, f"写异常: {e}")
                self.stop = True
                break
            except Exception as e:
                self.print(Com.message_type.info, f"异常: {e}")
                self.stop = True
                break
        self.thread.write = None

    def read(self):
        while not self.stop:
            try:
                data = self.serial.read(1)
                if data == b"":
                    continue
                data += self.serial.read(self.serial.in_waiting)
                data = data.decode("utf-8", errors="ignore")  # .strip()
                self.data.read = data
                self.print(Com.message_type.input, f"{data}")
            except serial.SerialException as e:
                self.print(Com.message_type.info, f"读异常: {e}")
                self.stop = True
                break
            except Exception as e:
                self.print(Com.message_type.info, f"异常: {e}")
                self.stop = True
                break
        self.thread.read = None

    def send(self, data):
        self.data.write += data

    def receive(self):
        while self.data.read == "":
            pass
        data = self.data.read
        self.data.read = ""
        return data


import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="串口通信工具")
    parser.add_argument("port", help="串口名称 (例如: COM23)")
    args = parser.parse_args()

    if re.fullmatch(r"COM\d+", args.port):
        print(f"连接到串口: {args.port}")
    else:
        print(f"无效的串口名称: {args.port}")
        parser.print_usage()
        sys.exit(-1)

    w = Com(args.port)
    w.connect()
    while True:
        try:
            w.send("test\n")
            response = w.receive()
            print(f"Response: {response}")
            time.sleep(1)
        except KeyboardInterrupt:
            w.disconnect()
            break
        except Exception as e:
            print(f"未知{e}")
            sys.exit(-1)

if False:
    coms = []
    while True:
        try:
            ports = serial.tools.list_ports.comports()
            for p in ports:
                if p.serial_number is None:
                    continue
                # print(p.device)
                t = Com(p.device)
                if t in coms:
                    continue
                coms.append(t)
                t.connect()

            x = [p.device for p in ports if p.serial_number is not None]
            for t in coms:
                if t.port not in x:
                    t.disconnect()
                    coms.remove(t)
            time.sleep(1)
        except KeyboardInterrupt:
            for t in coms:
                t.disconnect()
            print("\n[Main] 程序已退出")
            exit(-1)
