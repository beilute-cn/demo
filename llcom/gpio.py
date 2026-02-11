import sys
import re

from enum import Enum, auto

from com import Com


class Pin(Enum):
    J1_11 = auto()
    low = auto()
    high = auto()


class Board:
    def __init__(self, port: str):
        self.com = Com(port)

    def active(self):
        return self.com.connect()

    def inactive(self):
        self.com.disconnect()

    def __getattribute__(self, name):
        if re.fullmatch(r"Pin\..*", name):
            k = self.pin(Pin["J1_11"])
            command = f"read_gpio {k}\n"
            self.com.send(command)
            t = self.com.receive()
            groups = re.search(
                f"Running command: {command}"
                + f"Read PIN:{k}\n"
                + r"(HIGH_LED_OFF|LOW_LED_ON)   PIN (HIGH|LOW)\n\n"
                + f"Finish command: {command}",
                t,
            )
            print(f"{groups=}")
            if groups:
                print(f"{t.group(2)=}")
            else:
                print("read fail")

        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if re.fullmatch(r"Pin\..*", name):
            k = self.pin(Pin["J1_11"])
            match (value):
                case Pin.high:
                    v = 1
                case Pin.low:
                    v = 0
                case _:
                    v = -1
                    print("未知")
            command = f"write_gpio {k} {v}\n"
            self.com.send(command)
            t = self.com.receive()
            if re.fullmatch(
                f"Running command: {command}"
                + f"Write PIN:{k}, Value:{v}\n\n"
                + f"Finish command: {command}",
                t,
            ):
                pass
            else:
                print(f"write fail")
        else:
            object.__setattr__(self, name, value)

    def pin(self, pin: Pin) -> int:
        match (pin):
            case Pin.J1_11:
                return (2 << 5) | 1
            case _:
                print(f"未知")
                return -1


pins = [Pin.J1_11]


def check_pin(write: Board, read: Board, pin: Pin):
    setattr(write, str(pin), Pin.low)
    if getattr(read, str(pin)) == Pin.low:
        pass
    else:
        print(f"111")
    setattr(write, str(pin), Pin.high)
    if getattr(read, str(pin)) == Pin.high:
        pass
    else:
        print(f"222")


if __name__ == "__main__":
    try:
        b1 = Board("COM4")
        b2 = Board("COM25")

        if not b1.active() or not b2.active():
            print(f"失败")
            sys.exit(-1)

        for pin in pins:
            check_pin(b1, b2, pin)
    except KeyboardInterrupt as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        b1.inactive()
        b2.inactive()
