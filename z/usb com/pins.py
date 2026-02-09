import threading
import serial.tools.list_ports
import time
import string
import random

import sys


# ports = serial.tools.list_ports.comports()
# for p in ports:
#     if p.serial_number is None:
#         continue
#     print(f"{p.device}")

# serial.Serial("COM5", 115200, timeout=1),


def write(a):
    while not a.stop:
        if a.tx:
            data = a.tx
            a.tx = ""
            print(f"\033[34m[{a.port}]\033[33m <- {data}\033[0m")
            data = data.encode("utf-8")
            a.serial.write(data)


def read(a):
    while not a.stop:
        data = a.serial.read(1)
        data += a.serial.read(a.serial.in_waiting)
        data = data.decode("utf-8", errors="ignore")
        print(f"\033[34m[{a.port}]\033[32m -> {data}\033[0m")
        a.rx += data


class A:
    def __init__(self, port):
        self.port = port
        self.stop = False
        self.write = None
        self.read = None
        self.serial = None
        self.tx = ""
        self.rx = ""
        self.first = True

    def __eq__(self, other):
        return self.port == other.port

    def active(self):
        self.serial = serial.Serial(self.port, 115200)
        self.stop = False
        self.write = threading.Thread(target=write, args=(self,), daemon=True)
        self.read = threading.Thread(target=read, args=(self,), daemon=True)
        self.write.start()
        self.read.start()
        return self

    def unactive(self):
        self.stop = True

    def send(self, message):
        self.tx += message

    def receive(self):
        while not self.rx:
            pass
        t = self.rx
        self.rx = ""
        return t


# a = A("COM4").active()
# b = A("COM23").active()

# 从命令行参数获取串口
if len(sys.argv) != 3:
    print("用法: python pins.py <串口1> <串口2>")
    print("示例: python pins.py COM4 COM23")
    exit(1)

port1 = sys.argv[1]
port2 = sys.argv[2]

print(f"正在连接串口: {port1} 和 {port2}")
a = A(port1).active()
b = A(port2).active()

if a is None or b is None:
    print("\033[31m串口连接失败\033[0m")
    exit(1)


# fmt: off
available = [
    [
        #0, 1,
        2, 3, 4, 5, 6, 7
    ],
    [0, 1, 2, 3, 8, 9, 10, 11, 12,],
    [
        # 0, 1,
        2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23,
    ],
    [ 0, 1, 2, 3, 12, 13, 14, 15, 27, 28,],
]
# fmt: on

pin_code = [
    *range(0x10, 0x1F + 1),
    *range(0x51, 0x54 + 1),
    *range(0x20, 0x2F + 1),
    *range(0x30, 0x3F + 1),
    *range(0x40, 0x4B + 1),
]

finished = []

for i in range(7, 13 + 1):
    for j in range(1, 6 + 1):
        pin_code.append(i << 4 | j)


for i in range(len(available)):
    for j in range(len(available[i])):
        for code in pin_code:
            if code in finished:
                continue
            flag = True
            for k in range(2):
                level = "HIGH" if k else "LOW"

                a.send(f"GPIO{i} PIN1{available[i][j]} {level}\n")
                if "done" not in a.receive():
                    print(
                        f"\033[31mError on set GPIO{i} PIN{available[i][j]} {level}\033[0m"
                    )

                b.send(f"sreset\n")
                if "Finish command" not in b.receive():
                    print(f"\033[31mError on <sreset> command\033[0m")

                b.send(f"reset_sw\n")
                if "Finish command" not in b.receive():
                    print(f"\033[31mError on <reset_sw> command\033[0m")

                b.send(f"PIN_ROUTING 00 00 00 {code:x}\n")
                if "Finish command" not in b.receive():
                    print(
                        f"\033[31mError on <PIN_ROUTING 00 00 00 {code:x}> command\033[0m"
                    )

                b.send(f"PIN_ROUTING 00 00 00 f1\n")
                if "Finish command" not in b.receive():
                    print(f"\033[31mError on <PIN_ROUTING 00 00 00 f1> command\033[0m")

                b.send(f"read_gpio 17\n")
                t = b.receive()
                if "Finish command" not in t:
                    print(f"\033[31mError on <read_gpio 17> command\033[0m")

                if level not in t:
                    flag = False
                    print(
                        f"\033[31mError on <read_gpio 17> command, expected LOW but got {t}\033[0m"
                    )
                    break
            if flag:
                finished.append(code)
                print(f"\033[32mPassed: GPIO{i} PIN{available[i][j]} {level}")
                break

while True:
    try:
        pass
    except KeyboardInterrupt:
        a.unactive()
        exit(-1)


if False:
    coms = []

    while True:
        try:
            ports = serial.tools.list_ports.comports()
            for p in ports:
                if p.serial_number is None:
                    continue
                # print(p.device)
                a = A(p.device)
                if a in coms:
                    continue
                coms.append(a)
                a.active()

            x = [p.device for p in ports if p.serial_number is not None]
            for t in coms:
                if t.port not in x:
                    t.unactive()
                    coms.remove(t)

            time.sleep(1)
        except KeyboardInterrupt:
            exit(-1)
