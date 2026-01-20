import ctypes
from ctypes import wintypes


class coord(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.SHORT),
        ("y", wintypes.SHORT),
    ]
