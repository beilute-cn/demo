from console import Console
from progress import Process
import re
import time


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
