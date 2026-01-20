import ctypes
from ctypes import wintypes
from enum import IntFlag
from tab import tab


from key_event_record import key_event_record
from mouse_event import mouse_event
from window_buffer_size_event import window_buffer_size_event
from menu_event import menu_event
from focus_event import focus_event


from which import which
from parse import parse


class event_type(IntFlag):
    _ignore_ = "mapping"

    KEY_EVENT = 0x0001
    MOUSE_EVENT = 0x0002
    MENU_EVENT = 0x0008
    FOCUS_EVENT = 0x0010
    WINDOW_BUFFER_SIZE_EVENT = 0x0004

    def __str__(self):
        return event_type.mapping.get(self.value, f"未知事件<{self.value}>")


event_type.mapping = {
    0x0010: "焦点事件",
    0x0001: "键盘事件",
    0x0008: "菜单事件",
    0x0002: "鼠标事件",
    0x0004: "窗口缓冲区大小事件",
}


class event(ctypes.Union):
    _fields_ = [
        ("key_event", key_event_record),
        ("mouse_event", mouse_event),
        ("window_buffer_size_event", window_buffer_size_event),
        ("menu_event", menu_event),
        ("focus_event", focus_event),
    ]


class _input_record(parse, which, ctypes.Structure):
    _fields_ = [
        ("event_type", wintypes.WORD),
        ("event", event),
    ]

    def which(self):
        match self.event_type:
            case event_type.FOCUS_EVENT.value:
                return self.event.focus_event
            case event_type.KEY_EVENT.value:
                return self.event.key_event
            case event_type.MENU_EVENT.value:
                return self.event.menu_event
            case event_type.MOUSE_EVENT.value:
                return self.event.mouse_event
            case event_type.WINDOW_BUFFER_SIZE_EVENT.value:
                return self.event.window_buffer_size_event
            case _:
                return None

    def parse(self):
        event = self.which()
        if event:
            event.parse()
        else:
            print(f"未知事件类型<{self.event_type}>")
            exit(-2)

    def __str__(self):
        tab.tab()
        t = str(self.which())
        tab.untab()

        return f"""\
{tab}事件类型： {event_type(self.event_type)}
{tab}事件：
{t}\
"""
        return f"""\
{tab}event_type = {event_type(self.event_type).name}
{tab}event =
{t}\
"""
