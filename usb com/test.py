import threading
import serial.tools.list_ports
import time
import string
import random

# west build examples/demo_apps/hello_world  -p=always --toolchain=iar -t=guiproject --config=debug -b=kw47evk -Dcore_id=cm33_core0 -d=build/hello_world_kw47evk_id

ports = serial.tools.list_ports.comports()
for p in ports:
    if p.serial_number is None:
        continue
    print(f"{p.device}")

# ser = serial.Serial("COM4", 115200, timeout=1)


characters = list(string.ascii_letters + string.digits)


def write(a):
    while not a.stop:
        if a.port == "COM4":
            pass
        else:
            random.shuffle(characters)
            str = "".join(characters[:10])
            a.serial.write(str.encode("utf-8"))
            print(f"[{a.port}] <- {str}")
        time.sleep(1)
    a.write = None
    if a.read is None:
        a.serial.close()


def read(a):
    while not a.stop:
        # print("1")
        if a.serial.in_waiting:
            data = a.serial.read(a.serial.in_waiting)
            print(f"[{a.port}] -> {data.decode('utf-8', errors='ignore').strip()}")
        time.sleep(0.1)
    a.read = None
    if a.write is None:
        a.serial.close()


class A:
    def __init__(self, port):
        self.port = port
        self.stop = False
        self.write = None
        self.read = None
        self.serial = None

    def __eq__(self, other):
        return self.port == other.port

    def active(self):
        self.serial = serial.Serial(self.port, 115200, timeout=1)
        self.stop = False
        self.write = threading.Thread(target=write, args=(self,), daemon=True)
        self.read = threading.Thread(target=read, args=(self,), daemon=True)
        self.write.start()
        self.read.start()

    def unactive(self):
        self.stop = True


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
