import ctypes
from coord import coord


class window_buffer_size_event(ctypes.Structure):
    _fields_ = [
        ("dw_size", coord),
    ]

    def parse(self):
        print(f"<\033[35m<{self.dw_size.x} * {self.dw_size.y}\033[0m>")
