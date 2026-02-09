import ctypes
from ctypes import wintypes


class menu_event(ctypes.Structure):
    _fields_ = [
        ("dw_command_id", wintypes.UINT),
    ]
