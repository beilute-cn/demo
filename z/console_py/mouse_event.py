import ctypes
from ctypes import wintypes


from coord import coord
from control import control


from all import all


class mouse_event(ctypes.Structure):
    _fields_ = [
        ("dw_mouse_position", coord),
        ("dw_button_state", wintypes.DWORD),
        ("dw_control_key_state", wintypes.DWORD),
        ("dw_event_flags", wintypes.DWORD),
    ]

    def parse(self):
        b = button(self.dw_button_state & 0xFFFF)
        t = flag(self.dw_event_flags).all()
        # 实际滚动方向
        if self.dw_event_flags & flag.wheele.value:
            s = flag.name[flag.wheele.value]
            t = [x for x in t if x not in s]
            if self.dw_button_state & (1 << 31):
                t.append("向下滚动")
            else:
                t.append("向上滚动")
        elif self.dw_event_flags & flag.horizontal.value:
            s = flag.name[flag.horizontal.value]
            t = [x for x in t if x not in s]
            if self.dw_button_state & (1 << 31):
                t.append("向左滚动")
            else:
                t.append("向右滚动")
        # 按键按下时移动 -> 拖拽
        if (len(b)) and (self.dw_event_flags & flag.move.value):
            s = flag.name[flag.move.value]
            t = [x for x in t if x not in s]
            t.append("拖拽")

        print(
            (f"" if (len(b) or len(t)) else f"\033[90m")
            + f"<"
            + f"{self.dw_mouse_position.x}, "
            + f"{self.dw_mouse_position.y}, "
            + f"{b} "
            + f"{t}"
            + f">\033[0m"
        )

    def __str__(self):
        return f"""\
鼠标位置：<{self.dw_mouse_position.x}, {self.dw_mouse_position.y}>
按钮状态：{button(self.dw_button_state&0xffff)}
控制键状态：{control(self.dw_control_key_state)}
事件标志：{flag(self.dw_event_flags)}\
"""


class button(all):

    left = 0x0001
    right = 0x0002
    left_2 = 0x0004
    left_3 = 0x0008
    left_4 = 0x0010


button.name = {
    button.left.value: ["left", "左键"],
    button.right.value: ["right", "右键"],
    button.left_2.value: ["left-2", "左二键"],
    button.left_3.value: ["left-3", "左三键"],
    button.left_4.value: ["left-4", "左四键"],
}

button._name = "鼠标按钮"


class flag(all):
    move = 0x0001
    double_click = 0x0002
    wheele = 0x0004
    horizontal = 0x0008

    def all(self, en_zh=1):
        r = []
        v = self.value
        for key, value in self.name.items():
            if v & key:
                r.append(value[1])
            v &= ~key
        if v & flag.wheele.value:
            pass
        if v:
            print(f"\033[31m还有未识别的{self._name}<{hex(v)}>\033[0m")
        return r

    def __str__(self):
        return "[" + " + ".join(self.all(1)) + "]"


flag.name = {
    flag.move.value: ["move", "移动"],
    flag.double_click.value: ["double_click", "双击"],
    flag.wheele.value: ["wheele", "滚轮"],
    flag.horizontal.value: ["horizontal", "水平滚轮"],
}


flag._name = "鼠标事件标志"
