import ctypes
from ctypes import wintypes
from parse import parse


class focus_event(parse, ctypes.Structure):
    _fields_ = [
        ("b_set_focus", wintypes.BOOL),
    ]

    def parse(self):
        print(
            f""
            + f"<"
            + (f"\033[0m获得焦点" if self.b_set_focus else "\033[90m失去焦点")
            + f"\033[0m>"
        )
